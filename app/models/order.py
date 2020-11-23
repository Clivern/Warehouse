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


class Order(models.Model):
    """Order Model"""

    EUR = "EUR"

    CURRENCY_CHOICES = (
        (EUR, 'EURO'),
    )

    client_name = models.CharField(max_length=60, verbose_name="ClientName")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="PaidAmount")
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default="eur", verbose_name="Currency")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    products = models.ManyToManyField('Product', through='OrderProducts', related_name='order')

    class Meta:
        db_table = "app_order"
