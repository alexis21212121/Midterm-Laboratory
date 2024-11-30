from django.contrib import admin
from .models import Category, Product, Order, OrderItem, UserProfile
from .models import CustomUser

admin.site.register(CustomUser)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock') 
    list_filter = ('categories',) 
    search_fields = ('name', 'description') 
    autocomplete_fields = ('categories',) 


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'status')
    list_filter = ('status', 'date')  
    search_fields = ('user__username',) 


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order__status',) 
    search_fields = ('product__name', 'order__id')  


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number', 'address')