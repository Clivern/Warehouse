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

import uuid

from faker import Faker
from django.test import TestCase
from django.db.models.deletion import ProtectedError

from app.tests.base import Base
from app.service.products_service import ProductsService
from app.service.orders_service import OrdersService
from app.repository.order_repository import OrderRepository
from app.repository.product_repository import ProductRepository
from app.repository.article_repository import ArticleRepository
from app.exceptions.invalid_request import InvalidRequest


class TestOrdersService(Base, TestCase):
    """TestOrdersService Class Test Cases"""

    def setUp(self):
        self.fake = Faker()
        self.article_repository = ArticleRepository()
        self.product_repository = ProductRepository()
        self.products_service = ProductsService()
        self.order_repository = OrderRepository()
        self.orders_service = OrdersService()

    def test_new_order(self):
        product1, product2 = self.add_test_products()

        order1 = self.orders_service.new_order({
            "client": {
                "name": "Joe1"
            },
            "products": [
                {"id": product1.id, "quantity": 2}
            ]
        })
        self.assertEqual(order1.client_name, "Joe1")
        self.assertEqual(self.orders_service.get_order_by_id(order1.id)["client"]["name"], "Joe1")

        order2 = self.orders_service.new_order({
            "client": {
                "name": "Joe2"
            },
            "products": [
                {"id": product1.id, "quantity": 1},
                {"id": product2.id, "quantity": 1}
            ]
        })
        self.assertEqual(order2.client_name, "Joe2")
        self.assertEqual(self.orders_service.get_order_by_id(order2.id)["client"]["name"], "Joe2")

        with self.assertRaises(InvalidRequest):
            self.orders_service.new_order({
                "client": {
                    "name": "Joe3"
                },
                "products": [
                    {"id": product1.id, "quantity": 1},
                    {"id": product2.id, "quantity": 1}
                ]
            })

        with self.assertRaises(InvalidRequest):
            self.orders_service.new_order({
                "client": {
                    "name": "Joe4"
                },
                "products": [
                    {"id": "33333", "quantity": 1},
                    {"id": product2.id, "quantity": 1}
                ]
            })

    def add_test_products(self):
        product1 = self.product_repository.insert_one({
            "name": "Dining Table",
            "price": 20.2,
            "currency": ProductRepository.EUR
        })

        product2 = self.product_repository.insert_one({
            "name": "Kitchen Table",
            "price": 40,
            "currency": ProductRepository.EUR
        })

        seats = self.article_repository.insert_one({
            "name": "seats",
            "identifier": str(uuid.uuid4()),
            "quantity": 15
        })

        tables = self.article_repository.insert_one({
            "name": "tables",
            "identifier": str(uuid.uuid4()),
            "quantity": 31
        })

        self.product_repository.add_product_article_with_ident(product1.id, seats.identifier, 2)
        self.product_repository.add_product_article_with_ident(product1.id, tables.identifier, 1)

        self.product_repository.add_product_article_with_ident(product2.id, seats.identifier, 4)
        self.product_repository.add_product_article_with_ident(product2.id, tables.identifier, 2)

        return product1, product2

    def test_delete_db_records_of_orders_articles_relation(self):
        product1 = self.product_repository.insert_one({
            "name": "Dining Table",
            "price": 20.2,
            "currency": ProductRepository.EUR
        })

        product2 = self.product_repository.insert_one({
            "name": "Kitchen Table",
            "price": 40,
            "currency": ProductRepository.EUR
        })

        seats = self.article_repository.insert_one({
            "name": "seats",
            "identifier": str(uuid.uuid4()),
            "quantity": 15
        })

        tables = self.article_repository.insert_one({
            "name": "tables",
            "identifier": str(uuid.uuid4()),
            "quantity": 31
        })

        self.product_repository.add_product_article_with_ident(product1.id, seats.identifier, 2)
        self.product_repository.add_product_article_with_ident(product1.id, tables.identifier, 1)

        self.product_repository.add_product_article_with_ident(product2.id, seats.identifier, 4)
        self.product_repository.add_product_article_with_ident(product2.id, tables.identifier, 2)

        # We can't delete articles if they have products attached
        with self.assertRaises(ProtectedError):
            self.article_repository.delete_one_by_id(seats.id)

        with self.assertRaises(ProtectedError):
            self.article_repository.delete_one_by_id(tables.id)

        # Delete products first
        self.assertTrue(self.product_repository.delete_one_by_id(product1.id))
        self.assertTrue(self.product_repository.delete_one_by_id(product2.id))

        # Then we can delete articles
        self.assertTrue(self.article_repository.delete_one_by_id(seats.id))
        self.assertTrue(self.article_repository.delete_one_by_id(tables.id))

    def test_delete_db_records_of_orders_products_relation(self):
        product1, product2 = self.add_test_products()

        order1 = self.orders_service.new_order({
            "client": {
                "name": "Joe1"
            },
            "products": [
                {"id": product1.id, "quantity": 1},
                {"id": product2.id, "quantity": 1}
            ]
        })

        # We can't delete products if they have orders attached
        with self.assertRaises(ProtectedError):
            self.product_repository.delete_one_by_id(product1.id)

        with self.assertRaises(ProtectedError):
            self.product_repository.delete_one_by_id(product2.id)

        # Delete order first
        self.assertTrue(self.order_repository.delete_one_by_id(order1.id))

        # Then we can delete products
        self.assertTrue(self.product_repository.delete_one_by_id(product1.id))
        self.assertTrue(self.product_repository.delete_one_by_id(product2.id))
