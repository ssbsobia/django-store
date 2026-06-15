from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Brand, Category, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'category',
        'price',
        'discount_price',
        'stock',
        'is_available',
        'created_at'
    )

    list_filter = (
        'brand',
        'category',
        'is_available',
        'created_at'
    )

    search_fields = (
        'name',
        'brand__name',
        'category__name'
    )

    list_editable = ('price', 'stock', 'is_available')

    readonly_fields = ('created_at',)

    fieldsets = (
        ("Basic Info", {
            'fields': ('name', 'brand', 'category', 'description', 'image')
        }),
        ("Pricing", {
            'fields': ('price', 'discount_price')
        }),
        ("Stock Info", {
            'fields': ('stock', 'is_available')
        }),
        ("Specifications", {
            'fields': ('ram', 'storage', 'color')
        }),
        ("Meta", {
            'fields': ('created_at',)
        }),
    )