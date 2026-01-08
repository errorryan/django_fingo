

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin 
from myapp import views

urlpatterns = [
  
    path('admin/', admin.site.urls),


# 🔐 Auth routes
    path('register/', views.view_register, name='register'),
    path('login/', views.view_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # 🧑‍💼 Admin routes
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    # 👤 User dashboard
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),

    # 🏠 Main site
    path('', views.view_index, name='index'),
    # path('home',views.home, name='home'),
    path('search/', views.search, name='search'),
    path('about/', views.about_website, name='about'),
    path('services/', views.services_website, name='services'),
    path('contact/', views.contact, name='contact'),

    # 🐟 CRUD Product Management
    path('create_product/', views.view_create_product, name='product'),
    path('view_products/', views.view_products, name='view_products'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    # 🛒 Product detail and orders
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/place-order/', views.place_order, name='place_order'),
    path('my_orders/', views.my_orders, name='my_orders'),

    # 👤 Profile
    path("profile/update/", views.update_profile, name="update_profile"),
    path("profile/", views.profile_view, name="profile"),

    # 🧰 Admin Product CRUD
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),

    # manage_orders
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('manage-orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('manage-orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('Completed_orders/', views.Completed_orders, name='Completed_orders'),
    path('my_completed-orders/', views.my_completed_orders, name='my_completed_orders'),
    path('order-history/', views.order_history, name='order_history'),

    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),

    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),

    path('cart/', views.cart_view, name="cart"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/remove/<int:item_id>/', views.remove_item, name="remove_item"),
    path('cart/move/<int:product_id>/', views.move_to_cart, name="move_to_cart"),

    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('user_notifications/', views.user_notifications, name='user_notifications'),
    path('admin_notifications/', views.admin_notifications, name='admin_notifications'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
