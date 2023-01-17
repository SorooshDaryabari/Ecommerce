from rest_framework.serializers import ModelSerializer
from products.models import (
    Category,
    Brand,
    Product,
    ProductImage,
    ProductComment,
)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
            "parent",
            "is_active",
        )


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "name",
            "slug",
            "is_active",
        )


class ProductCommentSerializer(ModelSerializer):
    class Meta:
        model = ProductComment
        fields = (
            "user",
            "product",
            "reply",
            "text",
            "created_at",
        )


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "image",
            "alt_text",
            "if_feature",
        )


class ProductSerializer(ModelSerializer):
    product_image = ProductImageSerializer(
        many=True,
        read_only=True,
        source="productimage_set"
    )
    product_comment = ProductCommentSerializer(
        many=True,
        read_only=True,
        source="productcomment_set"
    )

    class Meta:
        model = Product
        fields = (
            "brand",
            "product_type",
            "category",
            "title",
            "descriptions",
            "slug",
            "regular_price",
            "discount_price",
            "is_active",
            "product_image",
            "product_comment",
        )


class ProductSearchSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "title",
            "slug",
            "regular_price",
            "discount_price",
            "short_description",
        )
