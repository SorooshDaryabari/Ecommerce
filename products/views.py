from products.serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductCommentSerializer,
    ProductSerializer,
)
from products.models import (
    Category,
    Brand,
    Product,
    ProductComment,
)
from rest_framework.viewsets import ModelViewSet
from products.permissions import IsStaffOrCommentCreatorOrReadOnly
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)
    permission_classes = (IsStaffOrCommentCreatorOrReadOnly,)
    lookup_field = "slug"


class BrandViewSet(ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.filter(is_active=True)
    permission_classes = (IsStaffOrCommentCreatorOrReadOnly,)
    lookup_field = "slug"


class ProductsByCategory(APIView):
    def get(self, request, slug=None):
        queryset = Product.objects.filter(category__slug__iexact=slug)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductsByBrand(APIView):
    def get(self, request, slug=None):
        queryset = Product.objects.filter(category__slug__iexact=slug)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCommentCreateView(CreateAPIView):
    serializer_class = ProductCommentSerializer
    permission_classes = (IsStaffOrCommentCreatorOrReadOnly,)
    queryset = ProductComment.objects.all()


class ProductCommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductCommentSerializer
    permission_classes = (IsStaffOrCommentCreatorOrReadOnly,)
    lookup_field = "id"

    def get_queryset(self):
        product_slug = self.kwargs.get("slug")
        return ProductComment.objects.filter(product__slug__iexact=product_slug)
