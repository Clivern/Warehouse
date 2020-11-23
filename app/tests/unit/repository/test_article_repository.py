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
from app.repository.article_repository import ArticleRepository


class TestArticleRepository(Base, TestCase):
    """TestArticleRepository Class"""

    def setUp(self):
        self.fake = Faker()
        self.article_repository = ArticleRepository()

    def test_insert_many(self):
        result = self.article_repository.insert_many([
            {"name": self.fake.word(), "identifier": str(uuid.uuid4()), "quantity": self.fake.pyint(1, 1000)},
            {"name": self.fake.word(), "identifier": str(uuid.uuid4()), "quantity": self.fake.pyint(1, 1000)},
            {"name": self.fake.word(), "identifier": str(uuid.uuid4()), "quantity": self.fake.pyint(1, 1000)},
            {"name": self.fake.word(), "identifier": str(uuid.uuid4()), "quantity": self.fake.pyint(1, 1000)},
        ])
        self.assertEqual(result, True)
        self.assertEqual(self.article_repository.count_all(), 4)

    def test_insert_one(self):
        result = self.article_repository.insert_one({
            "name": self.fake.word(),
            "identifier": str(uuid.uuid4()),
            "quantity": self.fake.pyint(1, 1000)
        })

        self.assertTrue(result.id > 0)
        self.assertEqual(self.article_repository.count_all(), 1)

    def test_delete_one_by_id(self):
        result = self.article_repository.insert_one({
            "name": self.fake.word(),
            "identifier": str(uuid.uuid4()),
            "quantity": self.fake.pyint(1, 1000)
        })

        self.assertTrue(result.id > 0)
        self.assertEqual(self.article_repository.count_all(), 1)
        self.assertTrue(self.article_repository.delete_one_by_id(result.id))
        self.assertEqual(self.article_repository.count_all(), 0)

    def test_update_one_by_id(self):
        result = self.article_repository.insert_one({
            "name": self.fake.word(),
            "identifier": str(uuid.uuid4()),
            "quantity": self.fake.pyint(1, 1000)
        })
        self.assertTrue(result.id > 0)

        name = self.fake.word()
        identifier = str(uuid.uuid4())
        quantity = self.fake.pyint(1, 1000)

        self.assertTrue(self.article_repository.update_one_by_id(result.id, {
            "name": name,
            "quantity": quantity,
            "identifier": identifier
        }))

        item = self.article_repository.get_one_by_id(result.id)
        self.assertEqual(name, item.name)
        self.assertEqual(identifier, item.identifier)
        self.assertEqual(quantity, item.quantity)

    def test_get_one_by_id(self):
        result = self.article_repository.insert_one({
            "name": self.fake.word(),
            "identifier": str(uuid.uuid4()),
            "quantity": self.fake.pyint(1, 1000)
        })

        item = self.article_repository.get_one_by_id(result.id)
        self.assertEqual(result.name, item.name)
        self.assertEqual(result.identifier, item.identifier)
        self.assertEqual(result.quantity, item.quantity)
        # Not found article
        self.assertFalse(self.article_repository.get_one_by_id(11111111111))

    def test_get_one_by_identifier(self):
        result = self.article_repository.insert_one({
            "name": self.fake.word(),
            "identifier": str(uuid.uuid4()),
            "quantity": self.fake.pyint(1, 1000)
        })

        item = self.article_repository.get_one_by_identifier(result.identifier)
        self.assertEqual(result.name, item.name)
        self.assertEqual(result.identifier, item.identifier)
        self.assertEqual(result.quantity, item.quantity)
        # Not found article
        self.assertFalse(self.article_repository.get_one_by_identifier("not-found"))

    def test_delete_all(self):
        self.article_repository.delete_all()
        self.assertEqual(self.article_repository.count_all(), 0)
        self.article_repository.insert_one({
            "name": self.fake.word(),
            "identifier": str(uuid.uuid4()),
            "quantity": self.fake.pyint(1, 1000)
        })
        self.assertEqual(self.article_repository.count_all(), 1)
