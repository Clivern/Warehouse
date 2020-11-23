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

import math

from django.db import models


class Product(models.Model):
    """Product Model"""

    EUR = "EUR"

    CURRENCY_CHOICES = (
        (EUR, 'EURO'),
    )

    name = models.CharField(max_length=60, verbose_name="Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default="eur", verbose_name="Currency")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    articles = models.ManyToManyField('Article', through='ProductArticles', related_name='product')

    @property
    def quantity(self):
        """Gets the quantity of the product based on current articles stock

        Returns:
            Integer equal the products number that can be made from current stock articles or None
            if it requires no articles
        """
        quantity = None

        # Get all product articles amounts (Linear Time Complexity)
        for article_amount in self.product_articles_amount.all():
            # It is always has to be more than zero (article quantity inside a product)
            if article_amount.quantity > 0:
                # Quantity should be the lowest number of products that can be made with the current
                # articles stock
                result = math.floor(article_amount.article.quantity / article_amount.quantity)
                if quantity is not None:
                    quantity = quantity if quantity < result else result
                else:
                    quantity = result

        return quantity

    def __str__(self):
        return self.name

    class Meta:
        db_table = "app_product"
