import factory
from accounts.models import (
    Account,
    Ticket,
    TickerAnswer,
    ShoppingCart,
    CartItem,
    Coupon,
)
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone_number = fake.phone_number()
    state = fake.state()
    city = fake.city()
    address = fake.street_address()
    zip_code = fake.zipcode()
    password = factory.PostGenerationMethodCall("set_password", "django")
    is_active = True
    is_supporter = False
    is_superuser = False
    is_staff = False


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    owner = factory.SubFactory(AccountFactory)
    title = "django"
    user_text = fake.text()
    created_at = datetime.now()


class TicketAnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TickerAnswer

    ticket = factory.SubFactory(TicketFactory)
    answer = fake.text()


class CouponFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Coupon

    title = "django"
    code = fake.uuid4()
    discount_price = 100
    start_at = datetime.now()
    end_at = datetime.now() + timedelta(0, 5)
    is_active = True
    created_at = datetime.now()


class ShoppingCartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShoppingCart

    owner = factory.SubFactory(AccountFactory)
    total = 12145.55
    coupon = factory.SubFactory(CouponFactory)
    created_at = datetime.now()
    is_paid = False


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(ShoppingCartFactory)
    price = 1225.89
    quantity = 5
