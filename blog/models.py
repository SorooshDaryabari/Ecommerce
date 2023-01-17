from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

POST_STATUS = (
    ("A", "Accepted"),
    ("C", "Checking"),
    ("P", "Pending"),
    ("R", "Rejected"),
)


class BlogCategory(MPTTModel):
    name = models.CharField(
        verbose_name=_("Category name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Category safe URL"),
        max_length=255,
        unique=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )
    is_active = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ("name",)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_("Tag"),
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_("Post title"),
        help_text=_("Required")
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name=_("Post safe URL"),
        help_text=_("Required"),
        unique=True
    )
    short_description = models.CharField(
        max_length=255,
        verbose_name=_("Short description"),
        help_text=_("Required")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Not required"),
        blank=True
    )
    category = models.ForeignKey(BlogCategory, on_delete=models.RESTRICT)
    post_status = models.CharField(
        choices=POST_STATUS,
        max_length=10,
        default=POST_STATUS[2][1]
    )
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    reply = models.ForeignKey(
        "Comment",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return "{} - {}".format(self.user.__str__(), self.post.title)


class PostImages(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_image",
        null=False,
        blank=False
    )
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to="images/blog/",
        default="images/blog/default.pnp",
    )
    alt_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text"),
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Post image")
        verbose_name_plural = _("Post images")
