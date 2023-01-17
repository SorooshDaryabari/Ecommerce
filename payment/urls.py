from django.urls import path
from payment.views import (
    go_to_gateway,
    call_back_gateway,
)

urlpatterns = [
    path("<int:id>/go-to-gateway/", go_to_gateway),
    path("<int:id>/call-back-gateway/", call_back_gateway),
]
