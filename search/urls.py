from django.urls import path
from search.views import (
    SearchProduct,
    SearchPost,
)
urlpatterns = [
    path("products/<str:query>/", SearchProduct.as_view()),
    path("posts/<str:query>/", SearchPost.as_view()),
]
