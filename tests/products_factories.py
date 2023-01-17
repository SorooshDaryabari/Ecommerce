import factory
from products.models import (
    Category,
    Brand,
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
    ProductComment,
)
from datetime import datetime
from faker import Faker

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "Django products category"
    slug = "django-products-category"
    is_active = True


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = "Brand"
    slug = "brand"
    is_active = True


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = "Digital"
    is_active = True


class ProductSpecificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    product_type = factory.SubFactory(ProductTypeFactory)
    name = "Color"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    brand = factory.SubFactory(BrandFactory)
    product_type = factory.SubFactory(ProductTypeFactory)
    category = factory.SubFactory(CategoryFactory)
    title = "Product"
    short_description = fake.text()
    description = fake.text()
    slug = "product"
    regular_price = 2599.59
    discount_price = 2499.99
    is_active = True
    created_at = datetime.now()


class ProductSpecificationValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = "Red"


class ProductCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductComment

    product = factory.SubFactory(ProductFactory)
    text = fake.text()
    created_at = datetime.now()
