from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, ProductImage, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'thumbnail')
    list_filter = ('category',)
    search_fields = ('name',)
    readonly_fields = ('thumbnail',)
    inlines = [ProductVariantInline, ProductImageInline]

    def thumbnail(self, obj):
        img = obj.image or (obj.images.first().image if obj.images.exists() else None)
        if img:
            return format_html("<img src='{}' style='height:48px'/>", img.url)
        return ''
    thumbnail.short_description = 'Preview'
