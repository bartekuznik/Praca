from django.contrib import admin
from .models import Category, Product, Profile, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'created', 'author']
    list_filter = ['available', 'created']
    list_editable = ['price','available']



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','description','image']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'days']