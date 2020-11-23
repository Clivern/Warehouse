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
from app.repository.article_repository import ArticleRepository
from app.exceptions.invalid_request import InvalidRequest


class ArticlesService():
    """ArticlesService Class

    Attributes:
        article_repository: an instance of article repository
        validator: an instance of validator class
    """

    def __init__(self):
        """Inits ArticlesService"""
        self.article_repository = ArticleRepository()
        self.validator = Validator()

    def load(self, data):
        """Loads a dict of articles into database

        Args:
            data: a dict containing articles data. For example
            {"inventory": [{"art_id": "1","name": "leg","stock": "12"}]}

        Returns:
            True on success and False on failure
        """
        batch = []

        # Filter out existed articles & raise error if passed stock value not integer
        for article in data["inventory"]:

            if self.article_repository.get_one_by_identifier(article["art_id"]) is not False:
                continue

            if not self.validator.is_positive_integer(article["stock"], 0):
                raise InvalidRequest(
                    _("Article with name {name} has invalid stock value").format(name=article["name"]),
                    HTTPStatus.BAD_REQUEST
                )

            batch.append({
                "name": article["name"],
                "identifier": article["art_id"],
                "quantity": int(article["stock"])
            })

        # Store Articles
        return self.article_repository.insert_many(batch)
