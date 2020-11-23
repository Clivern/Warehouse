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

import json

from django.test import TestCase
from django.shortcuts import reverse

from app.tests.base import Base
from app.repository.product_repository import ProductRepository
from app.repository.article_repository import ArticleRepository


class TestLoad(Base, TestCase):
    """TestLoad Class"""

    def setUp(self):
        self.article_repository = ArticleRepository()
        self.product_repository = ProductRepository()

    def test_load_articles_success(self):
        response = self.client.post(reverse("app.api.v1.load_inventory.endpoint"), json.dumps({
            "inventory": [
                {
                    "art_id": "1",
                    "name": "leg",
                    "stock": "12"
                },
                {
                    "art_id": "2",
                    "name": "screw",
                    "stock": "17"
                },
                {
                    "art_id": "3",
                    "name": "seat",
                    "stock": "2"
                },
                {
                    "art_id": "4",
                    "name": "table top",
                    "stock": "1"
                }
            ]
        }), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.article_repository.count_all(), 4)

    def test_load_articles_failure_01(self):
        response = self.client.post(reverse("app.api.v1.load_inventory.endpoint"), json.dumps({
            "inventory": [
                {
                    "art_id": "",
                    "name": "leg",
                    "stock": "12"
                },
                {
                    "art_id": "2",
                    "name": "screw",
                    "stock": "17"
                },
                {
                    "art_id": "3",
                    "name": "seat",
                    "stock": "2"
                },
                {
                    "art_id": "4",
                    "name": "table top",
                    "stock": "1"
                }
            ]
        }), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.article_repository.count_all(), 0)

    def test_load_articles_failure_02(self):
        response = self.client.post(
            reverse("app.api.v1.load_inventory.endpoint"),
            '{"faulty":"json}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.article_repository.count_all(), 0)

    def test_load_products_success(self):
        self.test_load_articles_success()
        response = self.client.post(reverse("app.api.v1.load_products.endpoint"), json.dumps({
            "products": [
                {
                    "name": "Dining Chair",
                    "contain_articles": [
                        {
                            "art_id": "1",
                            "amount_of": "4"
                        },
                        {
                            "art_id": "2",
                            "amount_of": "8"
                        },
                        {
                            "art_id": "3",
                            "amount_of": "1"
                        }
                    ]
                },
                {
                    "name": "Dinning Table",
                    "contain_articles": [
                        {
                            "art_id": "1",
                            "amount_of": "4"
                        },
                        {
                            "art_id": "2",
                            "amount_of": "8"
                        },
                        {
                            "art_id": "4",
                            "amount_of": "1"
                        }
                    ]
                }
            ]
        }), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.product_repository.count_all(), 2)

    def test_load_products_failure_01(self):
        self.test_load_articles_success()
        response = self.client.post(reverse("app.api.v1.load_products.endpoint"), json.dumps({
            "products": [
                {
                    "name": "Dining Chair",
                    "contain_articles": [
                        {
                            "art_id": "1",
                            "amount_of": "f"
                        },
                        {
                            "art_id": "2",
                            "amount_of": "8"
                        },
                        {
                            "art_id": "3",
                            "amount_of": "1"
                        }
                    ]
                },
                {
                    "name": "Dinning Table",
                    "contain_articles": [
                        {
                            "art_id": "1",
                            "amount_of": "4"
                        },
                        {
                            "art_id": "2",
                            "amount_of": "8"
                        },
                        {
                            "art_id": "4",
                            "amount_of": "1"
                        }
                    ]
                }
            ]
        }), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.product_repository.count_all(), 0)

    def test_load_products_failure_02(self):
        self.test_load_articles_success()
        response = self.client.post(reverse("app.api.v1.load_products.endpoint"), json.dumps({
            "products": [
                {
                    "name": "Dining Chair",
                    "contain_articles": [
                        {
                            "art_id": "1345",
                            "amount_of": "2"
                        },
                        {
                            "art_id": "2",
                            "amount_of": "8"
                        },
                        {
                            "art_id": "3",
                            "amount_of": "1"
                        }
                    ]
                },
                {
                    "name": "Dinning Table",
                    "contain_articles": [
                        {
                            "art_id": "1",
                            "amount_of": "4"
                        },
                        {
                            "art_id": "2",
                            "amount_of": "8"
                        },
                        {
                            "art_id": "4",
                            "amount_of": "1"
                        }
                    ]
                }
            ]
        }), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.product_repository.count_all(), 0)

    def test_load_products_failure_03(self):
        self.test_load_articles_success()
        response = self.client.post(
            reverse("app.api.v1.load_products.endpoint"),
            '{"faulty":"json}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.product_repository.count_all(), 0)
