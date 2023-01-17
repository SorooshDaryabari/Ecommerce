import pytest
from django.contrib.auth import get_user_model
from accounts.models import (
    Ticket,
    TickerAnswer,
    ShoppingCart,
    CartItem,
    Coupon,
)
from products.models import Product
from django.utils import timezone


@pytest.mark.parametrize(
    "username, first_name, last_name, email, phone_number, state, city, address, zip_code, password",
    [
        (
                "test1",
                "First name 1",
                "Last name 1",
                "test1@gmail.com",
                "+91 12345678901",
                "Florida",
                "Miami",
                "Street X",
                "33126",
                "password1",
        ),
        (
                "test2",
                "First name 2",
                "Last name 2",
                "test2@gmail.com",
                "+91 12345678902",
                "Texas",
                "Austin",
                "Street Y",
                "78653",
                "password2",
        ),
    ],
)
def test_account(
        db,
        account_factory,
        username,
        first_name,
        last_name,
        email,
        phone_number,
        state,
        city,
        address,
        zip_code,
        password,
):
    test = account_factory(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        state=state,
        city=city,
        address=address,
        zip_code=zip_code,
        password=password,
    )

    account = get_user_model().objects.all().first()

    assert account.username == test.username
    assert account.first_name == test.first_name
    assert account.last_name == test.last_name
    assert account.email == test.email
    assert account.phone_number == test.phone_number
    assert account.state == test.state
    assert account.city == test.city
    assert account.address == test.address
    assert account.zip_code == test.zip_code
    assert account.check_password(password)


@pytest.mark.parametrize(
    "title, user_text, created_at",
    [
        ("Test 1", "User text 1", timezone.now()),
        ("Test 2", "User text 2", timezone.now()),
    ],
)
def test_ticket(db, ticket_factory, account_factory, title, user_text, created_at):
    account_test = account_factory()
    test = ticket_factory(
        owner=account_test,
        title=title,
        user_text=user_text,
        created_at=created_at,
    )

    account = get_user_model().objects.all().first()
    ticket = Ticket.objects.all().first()

    assert ticket.owner == account
    assert ticket.title == test.title
    assert ticket.user_text == test.user_text
    assert ticket.created_at == test.created_at


@pytest.mark.parametrize(
    "answer",
    [
        ("Answer 1",),
        ("Answer 2",),
    ],
)
def test_ticket_answer(db, ticket_answer_factory, ticket_factory, answer):
    ticket_test = ticket_factory()
    test = ticket_answer_factory(
        ticket=ticket_test,
        answer=answer,
    )

    ticket = Ticket.objects.all().first()
    answer = TickerAnswer.objects.all().first()

    assert answer.ticket == ticket
    assert answer.answer == str(test.answer)


@pytest.mark.parametrize(
    "created_at, is_paid",
    [
        (timezone.now(), True),
        (timezone.now(), False),
    ],
)
def test_shopping_cart_group(
        db,
        account_factory,
        shopping_cart_factory,
        cart_item_factory,
        product_factory,
        coupon_factory,
        created_at,
        is_paid,
):
    account_test = account_factory()
    coupon_test = coupon_factory()
    product_test = product_factory()
    test = shopping_cart_factory(
        owner=account_test,
        coupon=coupon_test,
        created_at=created_at,
        is_paid=is_paid,
    )
    cart_item_test = cart_item_factory(
        cart=test,
        product=product_test,
        price=10000,
        quantity=5,
    )

    account = get_user_model().objects.all().first()
    coupon = Coupon.objects.all().first()
    shopping_cart = ShoppingCart.objects.all().first()
    cart_item = CartItem.objects.all().first()
    product = Product.objects.all().first()

    assert shopping_cart.owner == account
    assert shopping_cart.coupon == coupon
    assert shopping_cart.total == test.total
    assert shopping_cart.created_at == test.created_at
    assert shopping_cart.is_paid == test.is_paid

    assert cart_item.cart == shopping_cart
    assert cart_item.product == product
    assert cart_item.price == cart_item_test.price
    assert cart_item.quantity == cart_item_test.quantity
