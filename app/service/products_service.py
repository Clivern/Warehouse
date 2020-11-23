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

from http import HTTPStatus

from django.utils.translation import gettext as _

from app.util.validator import Validator
from app.repository.product_repository import ProductRepository
from app.repository.article_repository import ArticleRepository
from app.exceptions.invalid_request import InvalidRequest


class ProductsService():
    """ProductsService Class

    Attributes:
        product_repository: an instance of product repository
        article_repository: an instance of article repository
        validator: an instance of validator class
    """

    def __init__(self):
        """Inits ProductsService"""
        self.product_repository = ProductRepository()
        self.article_repository = ArticleRepository()
        self.validator = Validator()

    def get_products(self, offset, limit=10):
        """Get products list

        Args:
            offset: the products list offset
            limit: the products limit

        Returns:
            A list of products
        """
        products = []
        items = self.product_repository.get_many(offset, limit)
        for item in items:
            products.append({
                "id": item.id,
                "name": item.name,
                "price": {
                    "amount": item.price,
                    "currency": item.currency
                },
                "createdAt": item.created_at,
                "updatedAt": item.updated_at,
                "quantity": item.quantity
            })

        return products

    def get_products_count(self):
        """Get products total count

        Returns:
            The number of products
        """
        return self.product_repository.count_all()

    def get_product_by_id(self, product_id):
        """Get product by id

        Args:
            product_id: the product id

        Returns:
            a dict of product data if product exists otherwise False
        """
        result = self.product_repository.get_one_by_id(product_id)

        if result is not False:
            return {
                "id": product_id,
                "name": result.name,
                "price": {
                    "amount": result.price,
                    "currency": result.currency
                },
                "createdAt": result.created_at,
                "updatedAt": result.updated_at,
                "quantity": result.quantity
            }
        return False

    def load(self, data):
        """Loads a dict of products into database

        Args:
            data: a dict containing products data. For example
            {"products": [{"name": "Dining Chair","contain_articles": [{"art_id": "1","amount_of": "4"}]}]}

        Returns:
            True on success and False on failure
        """
        batch = []

        # Filter out existed products & raise error if passed stock value not integer or article don't exist
        for product in data["products"]:
            product_exists = self.product_repository.get_one_by_name(product["name"])

            if product_exists is not False:
                continue

            # Add product to the batch
            batch.append({
                "name": product["name"],
                "price": "20",
                "currency": ProductRepository.EUR,
                "contain_articles": []
            })

            for contained_article in product["contain_articles"]:

                if self.article_repository.get_one_by_identifier(contained_article["art_id"]) is False:
                    raise InvalidRequest(
                        _("Article with identifier {id} not found").format(id=contained_article["art_id"]),
                        HTTPStatus.BAD_REQUEST
                    )

                if not self.validator.is_positive_integer(contained_article["amount_of"], 1):
                    raise InvalidRequest(
                        _("Article with identifier {id} has invalid stock value").format(id=contained_article["art_id"]),
                        HTTPStatus.BAD_REQUEST
                    )
                # Add product articles to the last product on the batch
                batch[len(batch) - 1]["contain_articles"].append({
                    "article_identifier": contained_article["art_id"],
                    "quantity": int(contained_article["amount_of"])
                })

        # Store products
        for product in batch:

            stored_product = self.product_repository.insert_one({
                "name": product["name"],
                "price": product["price"],
                "currency": product["currency"]
            })

            self.product_repository.add_product_articles(stored_product.id, product["contain_articles"])

        return True
