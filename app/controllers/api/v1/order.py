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
from django.http import JsonResponse
from django.utils.translation import gettext as _

from app.util.validator import Validator
from app.controllers.controller import Controller
from app.service.orders_service import OrdersService
from app.exceptions.resource_not_found import ResourceNotFound
from app.exceptions.invalid_request import InvalidRequest


class Orders(View, Controller):
    """Orders Controller

    Attributes:
        orders_service: an instance of orders service
        validator: an instance of validator class
    """

    def __init__(self):
        self.orders_service = OrdersService()
        self.validator = Validator()

    def post(self, request):
        """Create Order"""
        # Validate request data
        result = self.validator.validate(
            request.body.decode('utf-8'),
            self.validator.get_schema_path("/schemas/api/v1/order/create.json")
        )

        if not result:
            raise InvalidRequest(
                self.validator.get_error(),
                HTTPStatus.BAD_REQUEST
            )

        new_order = self.orders_service.new_order(json.loads(request.body.decode('utf-8')))

        return JsonResponse(
            self.orders_service.get_order_by_id(new_order.id),
            status=HTTPStatus.CREATED
        )


class Order(View, Controller):
    """Order Controller

    Attributes:
        orders_service: an instance of orders service
    """

    def __init__(self):
        self.orders_service = OrdersService()

    def get(self, request, order_id):
        """Get order by id"""
        order = self.orders_service.get_order_by_id(int(order_id))

        if order is False:
            raise ResourceNotFound(
                _("Order with id {id} not found").format(id=int(order_id)),
                HTTPStatus.NOT_FOUND
            )

        return JsonResponse(order)
