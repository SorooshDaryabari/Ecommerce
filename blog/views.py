from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from blog.models import (
    BlogCategory,
    Post,
    Comment,
)
from blog.serializers import (
    CategorySerializer,
    PostSerializer,
    CommentSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from products.permissions import IsStaffOrCommentCreatorOrReadOnly


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = BlogCategory.objects.filter(is_active=True)
    permission_classes = (IsStaffOrCommentCreatorOrReadOnly,)
    lookup_field = "slug"


class PostsByCategory(APIView):
    def get(self, request, slug=None):
        queryset = Post.objects.filter(category__slug__iexact=slug)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(post_status="A")
    permission_classes = (IsStaffOrCommentCreatorOrReadOnly,)
    lookup_field = "slug"


class PostCommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrCommentCreatorOrReadOnly,)
    queryset = Comment.objects.all()


class PostCommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrCommentCreatorOrReadOnly,)
    lookup_field = "id"

    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Comment.objects.filter(post__slug__iexact=post_slug)
