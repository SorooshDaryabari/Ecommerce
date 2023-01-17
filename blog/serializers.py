from rest_framework import serializers
from blog.models import (
    BlogCategory,
    Post,
    PostImages,
    Comment,
    Tag,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = (
            "name",
            "slug",
            "parent",
            "is_active",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "reply",
            "post",
            "user",
            "text",
            "created_at",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class PostImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = (
            "image",
            "alt_text",
        )


class PostSerializer(serializers.ModelSerializer):
    post_images = PostImagesSerializer(
        many=True,
        read_only=True,
        source="postimage_set",
    )
    post_comments = CommentSerializer(
        many=True,
        read_only=True,
        source="comment_set",
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "category",
            "tags",
            "updated_at",
            "post_images",
            "post_comments",
        )


class PostSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "title",
            "short_description",
        )
