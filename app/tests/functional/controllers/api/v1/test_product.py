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

from django.test import TestCase
from django.shortcuts import reverse
from faker import Faker

from app.tests.base import Base
from app.repository.product_repository import ProductRepository
from app.repository.article_repository import ArticleRepository


class TestProduct(Base, TestCase):
    """TestProduct Class"""

    def setUp(self):
        self.fake = Faker()
        self.article_repository = ArticleRepository()
        self.product_repository = ProductRepository()

    def test_get_many(self):
        self.add_test_product()
        response = self.client.get(reverse("app.api.v1.products.endpoint"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue("\"quantity\": 5" in str(response.content))
        self.assertTrue("Dining Table" in str(response.content))

    def test_get_one_success(self):
        product = self.add_test_product()

        response = self.client.get(reverse("app.api.v1.product.endpoint", kwargs={'product_id': product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("\"quantity\": 5" in str(response.content))
        self.assertTrue("Dining Table" in str(response.content))

    def test_get_one_failure(self):
        response = self.client.get(reverse("app.api.v1.product.endpoint", kwargs={'product_id': 20}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue("Product with id 20 not found" in str(response.content))

    def add_test_product(self):
        product = self.product_repository.insert_one({
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

        self.product_repository.add_product_article_with_ident(product.id, seats.identifier, 2)
        self.product_repository.add_product_article_with_ident(product.id, tables.identifier, 1)

        return product
