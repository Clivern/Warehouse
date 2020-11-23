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
from app.repository.product_repository import ProductRepository
from app.repository.article_repository import ArticleRepository


class TestProductRepository(Base, TestCase):
    """TestProductRepository Class"""

    def setUp(self):
        self.fake = Faker()
        self.article_repository = ArticleRepository()
        self.product_repository = ProductRepository()

    def test_insert_many(self):
        result = self.product_repository.insert_many([
            {"name": self.fake.word(), "price": self.fake.pydecimal(
                right_digits=2,
                positive=True,
                min_value=10,
                max_value=50000
            ), "currency": ProductRepository.EUR},
            {"name": self.fake.word(), "price": self.fake.pydecimal(
                right_digits=2,
                positive=True,
                min_value=10,
                max_value=50000
            ), "currency": ProductRepository.EUR},
            {"name": self.fake.word(), "price": self.fake.pydecimal(
                right_digits=2,
                positive=True,
                min_value=10,
                max_value=50000
            ), "currency": ProductRepository.EUR},
            {"name": self.fake.word(), "price": self.fake.pydecimal(
                right_digits=2,
                positive=True,
                min_value=10,
                max_value=50000
            ), "currency": ProductRepository.EUR},
        ])
        self.assertEqual(result, True)
        self.assertEqual(self.product_repository.count_all(), 4)

    def test_insert_one(self):
        result = self.product_repository.insert_one({
            "name": self.fake.word(),
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        self.assertTrue(result.id > 0)
        self.assertEqual(self.product_repository.count_all(), 1)

    def test_delete_one_by_id(self):
        result = self.product_repository.insert_one({
            "name": self.fake.word(),
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        self.assertTrue(result.id > 0)
        self.assertEqual(self.product_repository.count_all(), 1)
        self.assertTrue(self.product_repository.delete_one_by_id(result.id))
        self.assertEqual(self.product_repository.count_all(), 0)

    def test_update_one_by_id(self):
        result = self.product_repository.insert_one({
            "name": self.fake.word(),
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })
        self.assertTrue(result.id > 0)

        name = self.fake.word()
        price = self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000)
        currency = ProductRepository.EUR

        self.assertTrue(self.product_repository.update_one_by_id(result.id, {
            "name": name,
            "currency": currency,
            "price": price
        }))

        item = self.product_repository.get_one_by_id(result.id)
        self.assertEqual(name, item.name)
        self.assertEqual(price, item.price)
        self.assertEqual(currency, item.currency)

    def test_get_one_by_id(self):
        result = self.product_repository.insert_one({
            "name": self.fake.word(),
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        item = self.product_repository.get_one_by_id(result.id)
        self.assertEqual(result.name, item.name)
        self.assertEqual(result.price, item.price)
        self.assertEqual(result.currency, item.currency)
        # Not found product
        self.assertFalse(self.product_repository.get_one_by_id(11111111111))

    def test_get_one_by_name(self):
        name = self.fake.word()

        result = self.product_repository.insert_one({
            "name": name,
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        item = self.product_repository.get_one_by_name(name)
        self.assertEqual(result.name, item.name)
        self.assertEqual(result.price, item.price)
        self.assertEqual(result.currency, item.currency)
        # Not found product
        self.assertFalse(self.product_repository.get_one_by_name("not-found"))

    def test_delete_all(self):
        self.product_repository.delete_all()
        self.assertEqual(self.product_repository.count_all(), 0)
        self.product_repository.insert_one({
            "name": self.fake.word(),
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })
        self.assertEqual(self.product_repository.count_all(), 1)

    def test_get_many(self):
        dinning_table = self.product_repository.insert_one({
            "name": "Dining Table",
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        work_office = self.product_repository.insert_one({
            "name": "Work Office",
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        kitchen_table = self.product_repository.insert_one({
            "name": "Kitchen Office",
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        seats = self.article_repository.insert_one({
            "name": "seats",
            "identifier": str(uuid.uuid4()),
            "quantity": 101
        })

        tables = self.article_repository.insert_one({
            "name": "tables",
            "identifier": str(uuid.uuid4()),
            "quantity": 31
        })

        self.assertTrue(self.product_repository.add_product_articles(dinning_table.id, [
            {"article_id": seats.id, "quantity": 3},
            {"article_identifier": tables.identifier, "quantity": 3}
        ]))

        self.assertTrue(self.product_repository.add_product_articles(work_office.id, [
            {"article_id": seats.id, "quantity": 3},
            {"article_identifier": tables.identifier, "quantity": 3}
        ]))

        self.assertTrue(self.product_repository.add_product_articles(kitchen_table.id, [
            {"article_id": seats.id, "quantity": 3},
            {"article_identifier": tables.identifier, "quantity": 3}
        ]))

        self.assertEqual(self.product_repository.get_one_by_id(dinning_table.id).quantity, 10)
        self.assertEqual(self.product_repository.get_one_by_id(work_office.id).quantity, 10)
        self.assertEqual(self.product_repository.get_one_by_id(kitchen_table.id).quantity, 10)

        self.assertEqual(len(self.product_repository.get_many(0, 1)), 1)
        self.assertEqual(len(self.product_repository.get_many(0, 3)), 3)
        self.assertEqual(len(self.product_repository.get_many(1, 1)), 1)
        self.assertEqual(len(self.product_repository.get_many(1, 2)), 2)
        self.assertEqual(len(self.product_repository.get_many(2, 4)), 1)

        # descending order
        self.assertEqual(self.product_repository.get_many(0, 3, '-created_at')[0].name, "Kitchen Office")

        # ascending order
        self.assertEqual(self.product_repository.get_many(0, 3, 'created_at')[0].name, "Dining Table")
        # descending order
        self.assertEqual(self.product_repository.get_many(0, 3, '-id')[0].name, "Kitchen Office")

        # ascending order
        self.assertEqual(self.product_repository.get_many(0, 3, 'id')[0].name, "Dining Table")

        # Sell 5 dinning tables
        self.product_repository.subtract_quantity_from_product(dinning_table.id, 5)
        self.assertEqual(self.product_repository.get_one_by_id(dinning_table.id).quantity, 5)

        # Sell another 2 dinning tables
        self.product_repository.subtract_quantity_from_product(dinning_table.id, 2)
        self.assertEqual(self.product_repository.get_one_by_id(dinning_table.id).quantity, 3)

    def test_add_product_article_with_ident(self):
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

        self.assertTrue(self.product_repository.add_product_article_with_ident(dinning_table.id, seats.identifier, 2).id > 0)
        self.assertTrue(self.product_repository.add_product_article_with_ident(dinning_table.id, tables.identifier, 1).id > 0)
        # Quantity should be 11 / 2
        self.assertEqual(self.product_repository.get_one_by_id(dinning_table.id).quantity, 5)
        self.assertEqual(
            self.product_repository.get_required_articles_for_product(dinning_table.id, 1),
            {seats.id: 2, tables.id: 1}
        )

    def test_add_product_article_with_id(self):
        dinning_table = self.product_repository.insert_one({
            "name": "Dining Table",
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        seats = self.article_repository.insert_one({
            "name": "seats",
            "identifier": str(uuid.uuid4()),
            "quantity": 101
        })

        tables = self.article_repository.insert_one({
            "name": "tables",
            "identifier": str(uuid.uuid4()),
            "quantity": 31
        })

        self.assertTrue(self.product_repository.add_product_article_with_id(dinning_table.id, seats.id, 2).id > 0)
        self.assertTrue(self.product_repository.add_product_article_with_id(dinning_table.id, tables.id, 1).id > 0)
        # Quantity should be 31 / 1
        self.assertEqual(self.product_repository.get_one_by_id(dinning_table.id).quantity, 31)

    def test_add_product_articles(self):
        dinning_table = self.product_repository.insert_one({
            "name": "Dining Table",
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        seats = self.article_repository.insert_one({
            "name": "seats",
            "identifier": str(uuid.uuid4()),
            "quantity": 101
        })

        tables = self.article_repository.insert_one({
            "name": "tables",
            "identifier": str(uuid.uuid4()),
            "quantity": 31
        })

        self.assertTrue(self.product_repository.add_product_articles(dinning_table.id, [
            {"article_id": seats.id, "quantity": 3},
            {"article_identifier": tables.identifier, "quantity": 3}
        ]))

        self.assertEqual(self.product_repository.get_one_by_id(dinning_table.id).quantity, 10)
