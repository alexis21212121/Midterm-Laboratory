from django.contrib import admin
from django.utils.html import format_html
from django.urls import path  # <-- Add this import
from django.shortcuts import render, redirect
from .models import Category, Product, Order, OrderItem, UserProfile, CustomUser, Cart

# Register CustomUser
admin.site.register(CustomUser)

# Register Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Register Product with Image Preview
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'display_image')  
    list_filter = ('categories',)  
    search_fields = ('name', 'description')  
    autocomplete_fields = ('categories',)  
    readonly_fields = ('display_image',)  

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50"/>', obj.image.url)
        return "No Image"
    
    display_image.short_description = "Product Image"

# Register Order with Status Update Actions
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username',)

    def get_urls(self):
        from django.urls import path  # Import path if not already done
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/update-status/', self.admin_site.admin_view(self.update_status), name='update_order_status'),
        ]
        return custom_urls + urls

    def update_status(self, request, order_id):
        order = Order.objects.get(id=order_id)
        if request.method == "POST":
            new_status = request.POST.get("status")
            order.status = new_status
            order.save()
            return redirect("/admin/app/order/")  # Redirect to the admin orders list page

        return render(request, "admin/app/update_order_status.html", {"order": order})

# Register the OrderAdmin class
admin.site.register(Order, OrderAdmin)

# Register OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order__status',)  
    search_fields = ('product__name', 'order__id')  

# Register UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number', 'address')

# Register Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')