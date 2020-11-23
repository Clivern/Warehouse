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

from django.core.exceptions import ObjectDoesNotExist

from app.models import Article


class ArticleRepository():
    """
    Article Repository class

    It encapsulate the logic required to access stored articles
    """

    def insert_many(self, articles_data):
        """Insert a batch of articles

        Args:
            articles_data: a list of articles data. For example
            [{"name": "..", "identifier": "..", "quantity": 1}]

        Returns:
            A boolean representing the success of the operation
        """
        articles = []
        for item in articles_data:
            articles.append(Article(
                name=item["name"],
                identifier=item["identifier"],
                quantity=item["quantity"]
            ))

        Article.objects.bulk_create(articles)

        return True

    def insert_one(self, article_data):
        """Insert a new article

        Args:
            article_data: a dict containing article data. For example
            {"name": "..", "identifier": "..", "quantity": 1}

        Returns:
            Article object in case of success and False on failure
        """
        article = Article()

        article.name = article_data["name"]
        article.identifier = article_data["identifier"]
        article.quantity = article_data["quantity"]

        article.save()
        return False if article.pk is None else article

    def delete_one_by_id(self, article_id):
        """Delete article by id

        Args:
            article_id: the article id

        Returns:
            True on success and False on failure
        """
        article = self.get_one_by_id(article_id)
        if article is not False:
            count, deleted = article.delete()
            return True if count > 0 else False
        return False

    def update_one_by_id(self, article_id, article_data):
        """Update article by id

        Args:
            article_id: the article id
            article_data: a dict containing article data

        Returns:
            True on success and False on failure
        """
        article = self.get_one_by_id(article_id)

        if article is not False:
            if "name" in article_data:
                article.name = article_data["name"]

            if "identifier" in article_data:
                article.identifier = article_data["identifier"]

            if "quantity" in article_data:
                article.quantity = article_data["quantity"]

            article.save()
            return True

        return False

    def get_one_by_id(self, article_id):
        """Get article by id

        Args:
            article_id: the article id

        Returns:
            Article object if article exists otherwise False
        """
        try:
            article = Article.objects.get(id=article_id)
            return False if article.pk is None else article
        except ObjectDoesNotExist:
            return False

    def get_one_by_identifier(self, article_identifier):
        """Get article by identifier

        Args:
            article_identifier: the article identifier

        Returns:
            Article object if article exists otherwise False
        """
        try:
            article = Article.objects.get(identifier=article_identifier)
            return False if article.pk is None else article
        except ObjectDoesNotExist:
            return False

    def count_all(self):
        """Get articles total count

        Returns:
            The number of articles
        """
        return Article.objects.count()

    def delete_all(self):
        """Delete all articles

        Returns:
            the number of articles deleted
        """
        return Article.objects.all().delete()
