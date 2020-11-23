# Copyright 2020 Clivern
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import functools
import operator
from http import HTTPStatus

from django.utils.translation import gettext as _

from app.repository.article_repository import ArticleRepository
from app.repository.product_repository import ProductRepository
from app.repository.order_repository import OrderRepository
from app.exceptions.invalid_request import InvalidRequest


class OrdersService():
    """OrdersService Class

    Attributes:
        article_repository: an instance of article repository
        product_repository: an instance of product repository
        order_repository: an instance of order repository
    """

    def __init__(self):
        """Inits OrdersService"""
        self.article_repository = ArticleRepository()
        self.product_repository = ProductRepository()
        self.order_repository = OrderRepository()

    def get_order_by_id(self, order_id):
        """Get order by id

        Args:
            order_id: the order id

        Returns:
            a dict of order data if order exists otherwise False
        """
        order = self.order_repository.get_one_by_id(order_id)

        if order is False:
            return False

        products = []

        for product in order.order_products_amount.all():
            products.append({"id": product.id, "name": product.product.name, "quantity": product.quantity})

        return {
            "id": order.id,
            "client": {
                "name": order.client_name
            },
            "payment": {
                "amount": order.paid_amount,
                "currency": order.currency
            },
            "createdAt": order.created_at,
            "updatedAt": order.updated_at,
            "products": products
        }

    def new_order(self, order_data):
        """Validate and store a new order

        Args:
            order_data: a dict containing order data. for example
            {"client": {"name": "clivern"}, "products": [{"id": 1, "quantity": 1},{"id": 2, "quantity": 1}]}

        Returns:
            Order object on success and False on failure

        Raises:
            InvalidRequest: Invalid order data or out of stock error
        """
        total_price = 0
        products = []

        for product_data in order_data["products"]:
            product = self.product_repository.get_one_by_id(int(product_data["id"]))

            if product is False:
                raise InvalidRequest(
                    _("Product with id {id} not found").format(id=int(product_data["id"])),
                    HTTPStatus.BAD_REQUEST
                )

            total_price += product.price
            products.append({
                "product_id": product.id,
                "quantity": product_data["quantity"]
            })

        # Check if current articles is sufficient
        if not self.check_products_availability(products):
            raise InvalidRequest(
                _("Sorry! Some of the ordered products are out of stock"),
                HTTPStatus.OK
            )

        # Store order data
        order = self.order_repository.insert_one({
            "client_name": order_data["client"]["name"],
            "paid_amount": total_price,
            "currency": ProductRepository.EUR
        })

        # Remove products from stock
        for product in products:
            self.product_repository.subtract_quantity_from_product(product["product_id"], product["quantity"])

        # Store ordered products
        self.order_repository.add_order_products(order.id, products)

        return order if order.id > 0 else False

    def check_products_availability(self, products):
        """Validate if a certain quantity of products can be ordered

        Args:
            products: a list of products data. for example
            [{"product_id": 1, "quantity": 1}, {"product_id": 2, "quantity": 2}]

        Returns:
            True if the quantity can be ordered and False otherwise
        """
        required_articles = []

        for product_data in products:
            required_articles.append(self.product_repository.get_required_articles_for_product(
                product_data["product_id"],
                product_data["quantity"]
            ))

        # Merge products requirements into one
        requirements = dict(functools.reduce(operator.add, map(collections.Counter, required_articles)))

        for article_id, needed_quantity in requirements.items():
            article = self.article_repository.get_one_by_id(article_id)
            if article.quantity < needed_quantity:
                return False

        return True
