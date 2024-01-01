from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlace, Wishlist

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'selling_price', 'category', 'product_image')

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'city', 'address', 'mobile')

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'order_id', 'payment_status', 'payment_id', 'paid')

@admin.register(OrderPlace)
class OrderPlaceModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'product', 'quantity', 'order_date', 'status', 'payment_mode')

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')