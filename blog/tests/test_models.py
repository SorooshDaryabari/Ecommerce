import pytest
from blog.models import (
    BlogCategory,
    Tag,
    Post,
    Comment,
)
from django.contrib.auth import get_user_model
from django.utils import timezone


@pytest.mark.parametrize(
    "name, slug, is_active",
    [
        ("Mobile", "mobile", True),
        ("Laptop", "laptop", False),
    ],
)
def test_blog_category(
        db, blog_category_factory, name, slug, is_active,
):
    test = blog_category_factory(
        name=name,
        slug=slug,
        is_active=is_active,
    )
    category = BlogCategory.objects.all().first()

    assert category.name == test.name
    assert category.slug == test.slug
    assert category.is_active == test.is_active


@pytest.mark.parametrize(
    "name",
    [
        ("Mobile",),
        ("Laptop",),
    ],
)
def test_tag(
        db, tag_factory, name,
):
    test = tag_factory(
        name=name,
    )
    tag = Tag.objects.all().first()
    assert tag.name == str(test.name)


@pytest.mark.parametrize(
    "title, slug, short_description, description, post_status, created_at,",
    [
        (
                "Artificial intelligence",
                "artificial-intelligence",
                "Short description1",
                "Description1",
                "C",
                timezone.now(),
        ),
        (
                "Hollywood",
                "hollywood",
                "Short description2",
                "Description2",
                "A",
                timezone.now(),
        ),
    ],
)
def test_post(
        db,
        post_factory,
        title,
        slug,
        short_description,
        description,
        post_status,
        created_at,
):
    test = post_factory(
        title=title,
        slug=slug,
        short_description=short_description,
        description=description,
        post_status=post_status,
        created_at=created_at,
    )

    post = Post.objects.all().first()

    assert post.title == test.title
    assert post.slug == test.slug
    assert post.short_description == test.short_description
    assert post.description == test.description
    assert post.post_status == test.post_status
    assert post.created_at == test.created_at


@pytest.mark.parametrize(
    "text, created_at",
    [
        ("Text1", timezone.now()),
        ("Text2", timezone.now()),
    ],
)
def test_comment(
        db, comment_factory, account_factory, text, created_at,
):
    test_user = account_factory()
    test = comment_factory(
        user=test_user,
        text=text,
        created_at=created_at,
    )

    comment = Comment.objects.all().first()
    user = get_user_model().objects.all().first()

    assert comment.user == user
    assert comment.text == test.text
    assert comment.created_at == test.created_at
