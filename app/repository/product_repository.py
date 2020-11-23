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

from app.models import Product
from app.models import ProductArticles
from app.models import Article


class ProductRepository():
    """
    Product Repository class

    It encapsulate the logic required to access stored products
    """

    EUR = Product.EUR

    def insert_many(self, products_data):
        """Insert a batch of products

        Args:
            products_data: a list of products data. For example
            [{"name": "..", "price": 20.20, "currency": "EUR"}]

        Returns:
            A boolean representing the success of the operation
        """
        products = []

        for item in products_data:
            products.append(Product(
                name=item["name"],
                price=item["price"],
                currency=item["currency"]
            ))

        Product.objects.bulk_create(products)

        return True

    def insert_one(self, product_data):
        """Insert a new product

        Args:
            product_data: a dict containing product data. For example
            {"name": "..", "price": 20, "currency": "EUR"}

        Returns:
            Product object in case of success and False on failure
        """
        product = Product()

        product.name = product_data["name"]
        product.price = product_data["price"]
        product.currency = product_data["currency"]

        product.save()
        return False if product.pk is None else product

    def delete_one_by_id(self, product_id):
        """Delete product by id

        Args:
            product_id: the product id

        Returns:
            True on success and False on failure
        """
        product = self.get_one_by_id(product_id)
        if product is not False:
            count, deleted = product.delete()
            return True if count > 0 else False
        return False

    def update_one_by_id(self, product_id, product_data):
        """Update product by id

        Args:
            product_id: the product id
            product_data: a dict containing product data

        Returns:
            True on success and False on failure
        """
        product = self.get_one_by_id(product_id)

        if product is not False:
            if "name" in product_data:
                product.name = product_data["name"]

            if "price" in product_data:
                product.price = product_data["price"]

            if "currency" in product_data:
                product.currency = product_data["currency"]

            product.save()
            return True

        return False

    def get_one_by_id(self, product_id):
        """Get product by id

        Args:
            product_id: the product id

        Returns:
            Product object if product exists otherwise False
        """
        try:
            product = Product.objects.get(id=product_id)
            return False if product.pk is None else product
        except ObjectDoesNotExist:
            return False

    def get_one_by_name(self, product_name):
        """Get product by id

        Args:
            product_name: the product name

        Returns:
            Product object if product exists otherwise False
        """
        try:
            product = Product.objects.get(name=product_name)
            return False if product.pk is None else product
        except ObjectDoesNotExist:
            return False

    def count_all(self):
        """Get products total count

        Returns:
            The number of products
        """
        return Product.objects.count()

    def delete_all(self):
        """Delete all products

        Returns:
            the number of products deleted
        """
        return Product.objects.all().delete()

    def get_many(self, offset, limit, order_by="-created_at"):
        """Get products list

        Args:
            offset: the products list offset
            limit: the products limit
            order_by: whether to order ascending or descending and with which column (eg. created_at or id)

        Returns:
            A list of products
        """
        if offset is None or limit is None:
            return Product.objects.order_by(order_by)

        return Product.objects.order_by(order_by)[offset:limit+offset]

    def add_product_article_with_ident(self, product_id, article_identifier, quantity):
        """Add article amount with identifier to a product

        Args:
            product_id: the product id
            article_identifier: the article identifier
            quantity: the article quantity

        Returns:
            Product object in case of success and False on failure
        """
        product_article = ProductArticles()

        product_article.article = Article.objects.get(identifier=article_identifier)
        product_article.product = Product.objects.get(pk=product_id)
        product_article.quantity = quantity

        product_article.save()
        return False if product_article.pk is None else product_article

    def add_product_article_with_id(self, product_id, article_id, quantity):
        """Add article amount with id to a product

        Args:
            product_id: the product id
            article_id: the article id
            quantity: the article quantity

        Returns:
            Product object in case of success and False on failure
        """
        product_article = ProductArticles()

        product_article.article = Article.objects.get(pk=article_id)
        product_article.product = Product.objects.get(pk=product_id)
        product_article.quantity = quantity

        product_article.save()
        return False if product_article.pk is None else product_article

    def add_product_articles(self, product_id, articles_data):
        """Add articles amounts to a product

        Args:
            product_id: the product id
            articles_data: a list of articles. for example
                [{"article_id": 1, "quantity":1}, {"article_identifier": "12", "quantity": 2}]

        Returns:
            True on success and False on failure
        """
        product_articles = []

        product = Product.objects.get(pk=product_id)

        for item in articles_data:
            if "article_id" in item:
                article = Article.objects.get(pk=item["article_id"])
            else:
                article = Article.objects.get(identifier=item["article_identifier"])

            product_articles.append(ProductArticles(
                article=article,
                product=product,
                quantity=item["quantity"]
            ))

        ProductArticles.objects.bulk_create(product_articles)

        return True

    def subtract_quantity_from_product(self, product_id, product_quantity):
        """Sell or remove a quantity of product and update the inventory accordingly

        Args:
            product_id: the product id
            product_quantity: the quantity to sell or remove
        """
        product = self.get_one_by_id(product_id)

        for article_amount in product.product_articles_amount.all():
            if article_amount.quantity > 0:
                # Update article quantity
                article_amount.article.quantity = article_amount.article.quantity - (article_amount.quantity * product_quantity)
                article_amount.article.save()

    def get_required_articles_for_product(self, product_id, product_quantity):
        """Get articles ids and total quantity needed to deliver a certain amount of product

        Args:
            product_id: the product id
            product_quantity: the quantity to sell or remove

        Returns:
            A dict or article id and quantity needed to build this product. for example
                {articleId: quantity_needed * product_quantity} -> {1: 2, 4: 3}
        """
        result = {}
        product = self.get_one_by_id(product_id)

        for article_amount in product.product_articles_amount.all():
            if article_amount.quantity > 0:
                if article_amount.article.id not in result.keys():
                    # Set quantity to zero
                    result[article_amount.article.id] = 0

                # Update article total quantity
                result[article_amount.article.id] += (article_amount.quantity * product_quantity)

        return result
