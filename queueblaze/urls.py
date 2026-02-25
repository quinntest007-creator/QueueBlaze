"""
URL configuration for queueblaze project.
Production-ready with WhiteNoise static files
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views
from main import admin as main_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Custom Admin URLs
    path('panel/login/', main_admin.admin_login, name='admin_login'),
    path('panel/logout/', main_admin.admin_logout, name='admin_logout'),
    path('panel/dashboard/', main_admin.admin_dashboard, name='admin_dashboard'),
    path('panel/products/', main_admin.admin_products, name='admin_products'),
    path('panel/products/add/', main_admin.admin_product_add, name='admin_product_add'),
    path('panel/products/edit/<int:product_id>/', main_admin.admin_product_edit, name='admin_product_edit'),
    path('panel/products/delete/<int:product_id>/', main_admin.admin_product_delete, name='admin_product_delete'),
    path('panel/orders/', main_admin.admin_orders, name='admin_orders'),
    path('panel/orders/<int:order_id>/', main_admin.admin_order_detail, name='admin_order_detail'),
    path('panel/orders/delete/<int:order_id>/', main_admin.admin_order_delete, name='admin_order_delete'),
    path('panel/settings/', main_admin.admin_settings, name='admin_settings'),
    
    # API URLs
    path('api/products/', main_admin.api_products, name='api_products'),
    path('api/settings/', main_admin.api_settings, name='api_settings'),
    path('api/save-order/', main_admin.save_order, name='save_order'),
    path('api/save-inquiry/', main_admin.save_inquiry, name='save_inquiry'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
