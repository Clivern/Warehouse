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

from django.core.exceptions import ObjectDoesNotExist

from app.models import Product
from app.models import Order
from app.models import OrderProducts


class OrderRepository():
    """
    Order Repository class

    It encapsulate the logic required to access stored orders
    """

    EUR = Order.EUR

    def insert_one(self, order_data):
        """Insert a new order

        Args:
            order_data: a dict containing article data. For example
            {"client_name": "..", "paid_amount": 20.20, "currency": "EUR"}

        Returns:
            Order object in case of success and False on failure
        """
        order = Order()

        order.client_name = order_data["client_name"]
        order.paid_amount = order_data["paid_amount"]
        order.currency = order_data["currency"]

        order.save()
        return False if order.pk is None else order

    def get_one_by_id(self, order_id):
        """Get order by id

        Args:
            order_id: the order id

        Returns:
            Order object if article exists otherwise False
        """
        try:
            order = Order.objects.get(id=order_id)
            return False if order.pk is None else order
        except ObjectDoesNotExist:
            return False

    def delete_one_by_id(self, order_id):
        """Delete order by id

        Args:
            order_id: the order id

        Returns:
            True on success and False on failure
        """
        order = self.get_one_by_id(order_id)
        if order is not False:
            count, deleted = order.delete()
            return True if count > 0 else False
        return False

    def add_order_products(self, order_id, products_data):
        """Add products to order

        Args:
            order_id: the order id
            products_data: a list of products data. for example
                [{"product_id": 1, "quantity": 2}]

        Returns:
            True on success and False on failure
        """
        product_articles = []

        order = Order.objects.get(pk=order_id)

        for item in products_data:
            product_articles.append(OrderProducts(
                order=order,
                product=Product.objects.get(pk=item["product_id"]),
                quantity=item["quantity"]
            ))

        OrderProducts.objects.bulk_create(product_articles)

        return True

    def delete_all(self):
        """Delete all orders

        Returns:
            the number of orders deleted
        """
        return Order.objects.all().delete()

    def count_all(self):
        """Get orders total count

        Returns:
            The number of orders
        """
        return Order.objects.count()
