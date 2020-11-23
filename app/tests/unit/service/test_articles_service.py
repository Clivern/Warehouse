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

from faker import Faker
from django.test import TestCase

from app.tests.base import Base
from app.service.articles_service import ArticlesService
from app.exceptions.invalid_request import InvalidRequest
from app.repository.article_repository import ArticleRepository


class TestArticlesService(Base, TestCase):
    """TestArticlesService Class Test Cases"""

    def setUp(self):
        self.fake = Faker()
        self.article_repository = ArticleRepository()
        self.articles_service = ArticlesService()

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

    def test_load_failure(self):
        with self.assertRaises(InvalidRequest):
            self.articles_service.load({
                "inventory": [
                    {
                        "art_id": "1",
                        "name": "leg",
                        "stock": ""
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
