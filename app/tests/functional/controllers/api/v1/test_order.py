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
from app.repository.order_repository import OrderRepository


class TestOrder(Base, TestCase):
    """TestOrder Class"""

    def setUp(self):
        self.article_repository = ArticleRepository()
        self.product_repository = ProductRepository()
        self.order_repository = OrderRepository()

    def test_create_order_success(self):
        self.load_articles_and_products()

        product1 = self.product_repository.get_one_by_name("Dining Chair")
        product2 = self.product_repository.get_one_by_name("Dinning Table")

        response = self.client.post(reverse("app.api.v1.orders.endpoint"), json.dumps({
            "client": {
                "name": "clivern"
            },
            "products": [
                {"id": product1.id, "quantity": 1},
                {"id": product2.id, "quantity": 1}
            ]
        }), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.order_repository.count_all(), 1)

        order_data = json.loads(response.content.decode('utf-8'))

        return order_data

    def test_create_order_failure_01(self):
        self.load_articles_and_products()

        product1 = self.product_repository.get_one_by_name("Dining Chair")
        product2 = self.product_repository.get_one_by_name("Dinning Table")

        response = self.client.post(reverse("app.api.v1.orders.endpoint"), json.dumps({
            "client": {
                "name": ""
            },
            "products": [
                {"id": product1.id, "quantity": 1},
                {"id": product2.id, "quantity": 1}
            ]
        }), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.order_repository.count_all(), 0)

    def test_create_order_failure_02(self):
        self.load_articles_and_products()

        product1 = self.product_repository.get_one_by_name("Dining Chair")
        product2 = self.product_repository.get_one_by_name("Dinning Table")

        response = self.client.post(reverse("app.api.v1.orders.endpoint"), json.dumps({
            "client": {
                "name": "clivern"
            },
            "products": [
                {"id": product1.id, "quantity": 2},
                {"id": product2.id, "quantity": 1}
            ]
        }), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.order_repository.count_all(), 0)

    def test_create_order_failure_03(self):
        self.load_articles_and_products()

        response = self.client.post(
            reverse("app.api.v1.orders.endpoint"),
            '{"faulty":"json}',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.order_repository.count_all(), 0)

    def test_get_order_success(self):
        order_data = self.test_create_order_success()
        response = self.client.get(reverse("app.api.v1.order.endpoint", kwargs={'order_id': order_data["id"]}))
        self.assertEqual(response.status_code, 200)

    def test_get_order_failure(self):
        self.test_create_order_success()
        response = self.client.get(reverse("app.api.v1.order.endpoint", kwargs={'order_id': 20}))
        self.assertEqual(response.status_code, 404)

    def load_articles_and_products(self):
        self.client.post(reverse("app.api.v1.load_inventory.endpoint"), json.dumps({
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

        self.client.post(reverse("app.api.v1.load_products.endpoint"), json.dumps({
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
