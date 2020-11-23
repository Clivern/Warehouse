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

from app.tests.base import Base
from app.repository.order_repository import OrderRepository
from app.repository.product_repository import ProductRepository
from app.repository.article_repository import ArticleRepository


class TestOrderRepository(Base, TestCase):
    """TestOrderRepository Class"""

    def setUp(self):
        self.fake = Faker()
        self.order_repository = OrderRepository()
        self.product_repository = ProductRepository()
        self.article_repository = ArticleRepository()

    def test_insert_one(self):
        self.assertTrue(self.order_repository.insert_one({
            "client_name": self.fake.word(),
            "paid_amount": self.fake.pydecimal(
                right_digits=2,
                positive=True,
                min_value=10,
                max_value=50000
            ),
            "currency": OrderRepository.EUR
        }).id > 0)

    def test_get_one_by_id(self):
        client_name = self.fake.word()

        order = self.order_repository.insert_one({
            "client_name": client_name,
            "paid_amount": self.fake.pydecimal(
                right_digits=2,
                positive=True,
                min_value=10,
                max_value=50000
            ),
            "currency": OrderRepository.EUR
        })

        self.assertEqual(self.order_repository.get_one_by_id(order.id).client_name, client_name)
        self.assertFalse(self.order_repository.get_one_by_id(1111111111111))

    def test_add_order_products(self):
        dinning_table = self.product_repository.insert_one({
            "name": "Dining Table",
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        seats = self.article_repository.insert_one({
            "name": "seats",
            "identifier": str(uuid.uuid4()),
            "quantity": 11
        })

        tables = self.article_repository.insert_one({
            "name": "tables",
            "identifier": str(uuid.uuid4()),
            "quantity": 31
        })

        self.product_repository.add_product_article_with_ident(dinning_table.id, seats.identifier, 2)
        self.product_repository.add_product_article_with_ident(dinning_table.id, tables.identifier, 1)

        order = self.order_repository.insert_one({
            "client_name": self.fake.word(),
            "paid_amount": self.fake.pydecimal(
                right_digits=2,
                positive=True,
                min_value=10,
                max_value=50000
            ),
            "currency": OrderRepository.EUR
        })

        self.order_repository.add_order_products(order.id, [
            {"product_id": dinning_table.id, "quantity": 3}
        ])

        attached_products = self.order_repository.get_one_by_id(order.id).products.all()
        self.assertEqual(attached_products[0].name, "Dining Table")
