from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Category(MPTTModel):
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Category safe URL"),
        unique=True,
        max_length=255,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    is_active = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ("name",)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(
        verbose_name=_("Brand Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Brand safe URL"),
        unique=True,
        max_length=255,
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Required"),
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.RESTRICT,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        help_text=_("Required"),
        unique=True,
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.RESTRICT,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Required"),
    )
    short_description = models.CharField(
        max_length=255,
        verbose_name=_("Short description"),
        help_text=_("Required"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Not Required"),
    )
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 4999.99$"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 4999.99$"),
            },
        },
        max_digits=6,
        decimal_places=2,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 4999.99$"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 4999.99$"),
            },
        },
        max_digits=6,
        decimal_places=2,
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    specification = models.ForeignKey(
        ProductSpecification,
        on_delete=models.RESTRICT,
    )
    value = models.CharField(
        max_length=255,
        verbose_name=_("Value"),
        help_text=_("Product specification value (maximum of 255"),
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a product image"),
        upload_to="images/products/",
        default="images/products/default.png",
    )
    alt_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text"),
    )
    if_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")


class ProductComment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    reply = models.ForeignKey(
        "ProductComment",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return "{} - {}".format(self.user.__str__(), self.product.title)
