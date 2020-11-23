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
from app.exceptions.invalid_request import InvalidRequest
from app.service.articles_service import ArticlesService
from app.service.products_service import ProductsService
from app.repository.product_repository import ProductRepository
from app.repository.article_repository import ArticleRepository


class TestProductsService(Base, TestCase):
    """TestProductsService Class Test Cases"""

    def setUp(self):
        self.fake = Faker()
        self.article_repository = ArticleRepository()
        self.product_repository = ProductRepository()
        self.products_service = ProductsService()
        self.articles_service = ArticlesService()

    def test_get_products(self):
        self.add_test_product()
        self.assertFalse(self.products_service.get_product_by_id(22222))
        self.assertEqual(self.products_service.get_products(0, 10)[0]["name"], "Dining Table")

    def test_get_products_count(self):
        self.add_test_product()
        self.assertEqual(self.products_service.get_products_count(), 1)

    def test_get_product_by_id(self):
        product = self.add_test_product()
        self.assertFalse(self.products_service.get_product_by_id(22222))
        self.assertEqual(self.products_service.get_product_by_id(product.id)["name"], "Dining Table")

    def test_get_product_without_articles_by_id(self):
        product = self.add_test_product_without_articles()
        self.assertFalse(self.products_service.get_product_by_id(22222))
        self.assertEqual(self.products_service.get_product_by_id(product.id)["quantity"], None)

    def test_load_success(self):
        self.articles_service.load({
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
        })
        self.assertEqual(self.article_repository.count_all(), 4)
        self.products_service.load({
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
        })
        self.assertEqual(self.products_service.get_products_count(), 2)

    def test_load_failure(self):
        self.articles_service.load({
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
        })
        self.assertEqual(self.article_repository.count_all(), 4)
        with self.assertRaises(InvalidRequest):
            self.products_service.load({
                "products": [
                    {
                        "name": "Dining Chair",
                        "contain_articles": [
                            {
                                "art_id": "1",
                                "amount_of": ""
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
            })

        with self.assertRaises(InvalidRequest):
            self.products_service.load({
                "products": [
                    {
                        "name": "Dining Chair",
                        "contain_articles": [
                            {
                                "art_id": "13",
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
            })

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

    def add_test_product_without_articles(self):
        product = self.product_repository.insert_one({
            "name": "Dining Table",
            "price": self.fake.pydecimal(right_digits=2, positive=True, min_value=10, max_value=50000),
            "currency": ProductRepository.EUR
        })

        return product
