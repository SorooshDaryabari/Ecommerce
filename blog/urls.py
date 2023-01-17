from rest_framework.routers import SimpleRouter
from blog.views import (
    CategoryViewSet,
    PostsByCategory,
    PostViewSet,
    PostCommentCreateView,
    PostCommentView,
)
from django.urls import path

router = SimpleRouter()

router.register("categories", CategoryViewSet)
router.register("posts", PostViewSet)

urlpatterns = [
    path(
        "categories/<slug:slug>/posts/",
        PostsByCategory.as_view(),
        name="posts-by-category",
    ),
    path(
        "comments/create/",
        PostCommentCreateView.as_view(),
        name="create-post-comment",
    ),
    path(
        "comments/<slug:slug>/<int:id>/",
        PostCommentView.as_view(),
        name="user-post-comment",
    ),
]

urlpatterns += router.urls
