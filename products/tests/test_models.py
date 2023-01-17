import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from products.models import (
    Category,
    Brand,
    ProductType,
    ProductSpecification,
    ProductSpecificationValue,
    Product,
    ProductComment,
)


@pytest.mark.parametrize(
    "name, slug, is_active",
    [
        ("Mobile", "mobile", False),
        ("Laptop", "laptop", True),
    ],
)
def test_category(db, category_factory, name, slug, is_active):
    test = category_factory(
        name=name,
        slug=slug,
        is_active=is_active,
    )
    category = Category.objects.all().first()

    assert category.name == test.name
    assert category.slug == test.slug
    assert category.is_active == test.is_active


@pytest.mark.parametrize(
    "name, slug, is_active",
    [
        ("Apple", "apple", True),
        ("Microsoft", "microsoft", False),
    ],
)
def test_category(db, brand_factory, name, slug, is_active):
    test = brand_factory(
        name=name,
        slug=slug,
        is_active=is_active,
    )
    brand = Brand.objects.all().first()

    assert brand.name == test.name
    assert brand.slug == test.slug
    assert brand.is_active == test.is_active


@pytest.mark.parametrize(
    "name, is_active",
    [
        ("Apple", True),
        ("Microsoft", False),
    ],
)
def test_product_type(db, product_type_factory, name, is_active):
    test = product_type_factory(
        name=name,
        is_active=is_active,
    )
    product_type = ProductType.objects.all().first()

    assert product_type.name == test.name
    assert product_type.is_active == test.is_active


@pytest.mark.parametrize(
    "name, is_active",
    [
        ("Apple", True),
        ("Microsoft", False),
    ],
)
def test_product_type(db, product_type_factory, name, is_active):
    test = product_type_factory(
        name=name,
        is_active=is_active,
    )
    product_type = ProductType.objects.all().first()

    assert product_type.name == test.name
    assert product_type.is_active == test.is_active


@pytest.mark.parametrize(
    "name",
    [
        ("Test1",),
        ("Test2",),
    ],
)
def test_product_specification(db, product_specification_factory, product_type_factory, name):
    product_type_test = product_type_factory()
    test = product_specification_factory(
        product_type=product_type_test,
        name=name,
    )

    product_type = ProductType.objects.all().first()
    product_specification = ProductSpecification.objects.all().first()

    assert product_specification.product_type == product_type
    assert product_specification.name == str(test.name)


@pytest.mark.parametrize(
    "title, short_description, description, slug, regular_price, discount_price, is_active, created_at",
    [
        (
                "Macbook pro 16",
                "Macbook pro 16 short description",
                "Macbook pro 16 description",
                "macbook-pro-16",
                2599.99,
                2399.99,
                True,
                timezone.now,
        ),
        (
                "Surface book 3",
                "Surface book 3 short description",
                "Surface book 3 description",
                "surface-book-3",
                1999.59,
                1899.59,
                False,
                timezone.now,
        ),
    ],
)
def test_product(
        db,
        product_factory,
        category_factory,
        brand_factory,
        product_type_factory,
        title,
        short_description,
        description,
        slug,
        regular_price,
        discount_price,
        is_active,
        created_at,
):
    category_test = category_factory()
    brand_test = brand_factory()
    product_type_test = product_type_factory()
    test = product_factory(
        brand=brand_test,
        product_type=product_type_test,
        category=category_test,
        title=title,
        short_description=short_description,
        description=description,
        slug=slug,
        regular_price=regular_price,
        discount_price=discount_price,
        is_active=is_active,
        created_at=created_at,
    )

    category = Category.objects.all().first()
    brand = Brand.objects.all().first()
    product_type = ProductType.objects.all().first()
    product = Product.objects.all().first()

    assert product.title == test.title
    assert product.short_description == test.short_description
    assert product.description == test.description
    assert product.slug == test.slug
    assert float(product.regular_price) == test.regular_price
    assert float(product.discount_price) == test.discount_price
    assert product.is_active == test.is_active
    assert product.created_at == test.created_at
    assert product.category == category
    assert product.brand == brand
    assert product.product_type == product_type


@pytest.mark.parametrize(
    "value",
    [
        ("Test 1",),
        ("Test 2",),
    ],
)
def test_product_specification_value(
        db,
        product_specification_value_factory,
        product_factory,
        product_specification_factory,
        value
):
    product_specification_test = product_specification_factory()
    product_test = product_factory()
    test = product_specification_value_factory(
        specification=product_specification_test,
        product=product_test,
        value=value,
    )

    product = Product.objects.all().first()
    product_specification = ProductSpecification.objects.all().first()
    product_specification_value = ProductSpecificationValue.objects.all().first()

    assert product_specification_value.specification == product_specification
    assert product_specification_value.product == product
    assert product_specification_value.value == str(test.value)


@pytest.mark.parametrize(
    "text",
    [
        ("Text 1",),
        ("Text 2",),
    ],
)
def test_product_specification_value(
        db,
        product_comment_factory,
        product_factory,
        account_factory,
        text,
):
    product_test = product_factory()
    account_test = account_factory()
    test = product_comment_factory(
        user=account_test,
        product=product_test,
        text=text,
    )

    account = get_user_model().objects.all().first()
    product = Product.objects.all().first()
    comment = ProductComment.objects.all().first()

    assert comment.user == account
    assert comment.product == product
    assert comment.text == str(test.text)
