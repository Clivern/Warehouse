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
from http import HTTPStatus

from django.views import View
from django.http import HttpResponse

from app.util.validator import Validator
from app.controllers.controller import Controller
from app.service.products_service import ProductsService
from app.service.articles_service import ArticlesService
from app.exceptions.invalid_request import InvalidRequest


class Articles(View, Controller):
    """Articles Controller

    Attributes:
        articles_service: an instance of articles service
        validator: an instance of validator class
    """

    def __init__(self):
        self.articles_service = ArticlesService()
        self.validator = Validator()

    def post(self, request):
        """Load Articles"""
        # Validate request data
        result = self.validator.validate(
            request.body.decode('utf-8'),
            self.validator.get_schema_path("/schemas/api/v1/article/load.json")
        )

        if not result:
            raise InvalidRequest(
                self.validator.get_error(),
                HTTPStatus.BAD_REQUEST
            )

        self.articles_service.load(json.loads(request.body.decode('utf-8')))

        return HttpResponse(status=HTTPStatus.CREATED)


class Products(View, Controller):
    """Products Controller

    Attributes:
        products_service: an instance of products service
        validator: an instance of validator class
    """

    def __init__(self):
        self.products_service = ProductsService()
        self.validator = Validator()

    def post(self, request):
        """Load Products"""
        # Validate request data
        result = self.validator.validate(
            request.body.decode('utf-8'),
            self.validator.get_schema_path("/schemas/api/v1/product/load.json")
        )

        if not result:
            raise InvalidRequest(
                self.validator.get_error(),
                HTTPStatus.BAD_REQUEST
            )

        self.products_service.load(json.loads(request.body.decode('utf-8')))

        return HttpResponse(status=HTTPStatus.CREATED)
