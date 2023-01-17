from rest_framework.routers import SimpleRouter
from products.views import (
    CategoryViewSet,
    ProductsByCategory,
    BrandViewSet,
    ProductsByBrand,
    ProductViewSet,
    ProductCommentCreateView,
    ProductCommentView,
)
from django.urls import path

router = SimpleRouter()
router.register("categories", CategoryViewSet)
router.register("brands", BrandViewSet)
router.register("products", ProductViewSet)

urlpatterns = [
    path(
        "categories/<slug:slug>/products/",
        ProductsByCategory.as_view(),
        name="products-by-category",
    ),
    path(
        "brands/<slug:slug>/products/",
        ProductsByBrand.as_view(),
        name="products-by-brand",
    ),
    path(
        "comments/create/",
        ProductCommentCreateView.as_view(),
        name="create-product-comment",
    ),
    path(
        "comments/<slug:slug>/<int:id>/",
        ProductCommentView.as_view(),
        name="user-create-comment",
    ),
]

urlpatterns += router.urls
