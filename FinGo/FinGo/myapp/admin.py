from django.contrib import admin
from .models import Product, Order, UserProfile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'productName', 'price', 'stock', 'created_at')
    search_fields = ('productName',)
    list_filter = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_user_address', 'product', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'product__productName')

    # ✅ Display the user's address from UserProfile
    def get_user_address(self, obj):
        if hasattr(obj.user, 'userprofile') and obj.user.userprofile.address:
            return obj.user.userprofile.address
        return "No address"
    get_user_address.short_description = 'Delivery Address'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_no', 'address', 'birthdate')
    search_fields = ('user__username', 'address')
