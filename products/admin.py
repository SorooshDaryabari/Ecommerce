from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from products.models import (
    Category,
    Brand,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
    ProductComment,
)

admin.site.register(Brand)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(ProductComment)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = (
        ProductSpecificationInline,
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (
        ProductImageInline,
        ProductSpecificationValueInline,
    )
