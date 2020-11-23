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

from django.urls import include, path

from app.controllers.web.home import Home
from app.controllers.web.health import Health
from app.controllers.api.v1.product import Product
from app.controllers.api.v1.product import Products
from app.controllers.api.v1.order import Order
from app.controllers.api.v1.order import Orders
from app.controllers.api.v1.load import Articles as LoadArticles
from app.controllers.api.v1.load import Products as LoadProducts
from app.controllers.web.error import handler404 as handler404_view
from app.controllers.web.error import handler500 as handler500_view


urlpatterns = [
    # Guest web pages
    path('', Home.as_view(), name='app.web.home'),
    path('_health', Health.as_view(), name='app.web.health'),

    # v1 API Endpoints
    path('api/v1/', include([
        # Endpoints to load inventory and products from JSON file
        path('load/articles', LoadArticles.as_view(), name='app.api.v1.load_inventory.endpoint'),
        path('load/products', LoadProducts.as_view(), name='app.api.v1.load_products.endpoint'),

        # REST Endpoints
        path('product', Products.as_view(), name='app.api.v1.products.endpoint'),
        path('product/<int:product_id>', Product.as_view(), name='app.api.v1.product.endpoint'),
        path('order', Orders.as_view(), name='app.api.v1.orders.endpoint'),
        path('order/<int:order_id>', Order.as_view(), name='app.api.v1.order.endpoint'),
    ]))
]

handler404 = handler404_view
handler500 = handler500_view
