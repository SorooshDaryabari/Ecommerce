from django.contrib.auth import (
    get_user_model,
)
from rest_framework import serializers
from accounts.models import (
    Account,
    ShoppingCart,
    CartItem,
    Ticket,
    TickerAnswer,
)
from accounts.tasks import send_email_activation_code_task
from django.utils.crypto import get_random_string


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Confirm password"}
    )
    first_name = serializers.CharField(
        write_only=True,
        required=True,
    )
    last_name = serializers.CharField(
        write_only=True,
        required=True,
    )
    email = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "state",
            "city",
            "address",
            "zip_code",
            "password",
            "confirm_password",
        )

    def create(self, validated_data):
        username = validated_data.get("username")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        email = validated_data.get("email")
        phone_number = validated_data.get("phone_number")
        state = validated_data.get("state")
        city = validated_data.get("city")
        address = validated_data.get("address")
        zip_code = validated_data.get("zip_code")
        email_unique_code = get_random_string(255)
        password = validated_data.get("password")

        user = get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            state=state,
            city=city,
            address=address,
            zip_code=zip_code,
            email_unique_code=email_unique_code,
            is_active=False,
        )
        user.set_password(password)
        user.save()

        full_name = f"{first_name} {last_name}"
        send_email_activation_code_task.delay(full_name, email, email_unique_code)

        return user

    def validate_password(self, value):
        data = self.get_initial()
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords must be match")
        return value


class AccountDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "state",
            "city",
            "address",
            "zip_code",
        )


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "password")


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            "cart",
            "product",
            "price",
            "quantity",
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = (
            "owner",
            "total",
            "created_at",
            "cart_items",
            "is_paid",
        )


class TicketAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TickerAnswer
        fields = ("answer",)


class TicketSerializer(serializers.ModelSerializer):
    answer = TicketAnswerSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "owner",
            "title",
            "user_text",
            "answer",
            "created_at",
        )
