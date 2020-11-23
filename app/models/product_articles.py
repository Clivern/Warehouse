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

from django.db import models

from .product import Product
from .article import Article


class ProductArticles(models.Model):
    """ProductArticles Model"""

    article = models.ForeignKey(
        Article,
        # Prevent deletion of an article if it is used by
        # any product
        on_delete=models.PROTECT,
        db_index=True,
        verbose_name="Related Article",
        related_name='product_articles_amount',
        null=False
    )

    product = models.ForeignKey(
        Product,
        # Delete if product got deleted
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Product",
        related_name='product_articles_amount',
        null=False
    )

    quantity = models.IntegerField(verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_product_articles"
