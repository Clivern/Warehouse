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
from .order import Order


class OrderProducts(models.Model):
    """OrderProducts Model"""

    order = models.ForeignKey(
        Order,
        # Delete if order got deleted
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Order",
        related_name='order_products_amount',
        null=False
    )

    product = models.ForeignKey(
        Product,
        # Prevent deletion of a product if it is still used by
        # any order
        on_delete=models.PROTECT,
        db_index=True,
        verbose_name="Related Product",
        related_name='order_products_amount',
        null=False
    )

    quantity = models.IntegerField(verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_order_poducts"
