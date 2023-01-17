import factory
from blog.models import (
    BlogCategory,
    Tag,
    Post,
    Comment,
)
from datetime import datetime
from faker import Faker

fake = Faker()


class BlogCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogCategory

    name = "Django blog category"
    slug = "django-blog-category"
    is_active = True


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = "tag"


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = "Django post title"
    slug = "django-post-slug"
    short_description = fake.text()
    description = fake.text()
    category = factory.SubFactory(BlogCategoryFactory)
    created_at = datetime.now()


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    user = 1
    text = fake.text()
    created_at = datetime.now()
