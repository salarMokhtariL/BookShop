from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(Language)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'gender', 'email']
    list_per_page = 10
    list_filter = ['name']
    list_editable = ['role']
    search_fields = ['name', 'role']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'rank']
    list_filter = ['rank']
    list_per_page = 10
    list_editable = ['rank']
    search_fields = ['name', 'rank']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'author_name',
                    'digital', 'in_stock', 'is_active']
    list_per_page = 10
    list_filter = ['price']
    list_editable = ['price', 'in_stock', 'digital', 'is_active']
    search_fields = ['title', 'author_name']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity', 'date_add']
    list_filter = ['quantity']
    list_editable = ['quantity']
    list_per_page = 10
    search_fields = ['order', 'product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'complete', 'transaction_id', 'date_order']
    list_filter = ['complete', 'customer']
    list_editable = ['complete']
    list_per_page = 10
    search_fields = ['transaction_id', 'customer']


@admin.register(Customer)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email']
    list_filter = ['user', 'name']
    list_editable = ['email']
    list_per_page = 10
    search_fields = ['name']
