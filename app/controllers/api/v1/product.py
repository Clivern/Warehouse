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

from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _

from app.controllers.controller import Controller
from app.service.products_service import ProductsService
from app.exceptions.resource_not_found import ResourceNotFound


class Products(View, Controller):
    """Products Controller

    Attributes:
        products_service: an instance of products service
    """

    def __init__(self):
        self.products_service = ProductsService()

    def get(self, request):
        """Get products list"""
        try:
            offset = int(request.GET.get('offset', 0))
            limit = int(request.GET.get('limit', 10))
        except Exception:
            offset = 0
            limit = 10

        return JsonResponse({
            'products': self.products_service.get_products(offset, limit),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'total': self.products_service.get_products_count()
            }
        })


class Product(View, Controller):
    """Product Controller

    Attributes:
        products_service: an instance of products service
    """

    def __init__(self):
        self.products_service = ProductsService()

    def get(self, request, product_id):
        """Get product by id"""
        product = self.products_service.get_product_by_id(int(product_id))

        if product is False:
            raise ResourceNotFound(
                _("Product with id {id} not found").format(id=int(product_id)),
                HTTPStatus.NOT_FOUND
            )

        return JsonResponse(product)
