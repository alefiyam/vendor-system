from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #vendors
    path('vendors/', views.vendors, name='vendors'),
    path('all_vendors/', views.all_vendors, name='all-vendors'),
    path('get_vendor/<str:vendor_id>/', views.get_vendor, name='get-vendors'),
    path('update_vendors/<str:vendor_id>/', views.update_vendors, name='update-vendors'),
    path('delete_vendors/<str:vendor_id>/delete/', views.delete_vendors, name='delete-vendors'),
    #purchase orders
    path('create_purchase_orders/', views.create_purchase_orders, name='create-purchase-orders'),
    path('all_purchase_orders/', views.all_purchase_orders, name='all-purchase-orders'),
     path('get_purchase_order/<str:po_number>/', views.get_purchase_order, name='get-purchase-order'),
    path('update_purchase_orders/<str:po_number>/', views.update_purchase_orders, name='update-purchase-orders'),
    path('delete_purchase_orders/<str:po_number>/delete/', views.delete_purchase_orders, name='delete-purchase-orders'),
    #Update Acknowledgment Endpoint
    path('purchase_orders/<str:po_number>/acknowledge/', views.acknowledge_purchase_orders, name='acknowledge-purchase-orders'),
    #Vendor Performance Endpoint
    path('vendor_performance/<str:vendor_id>/performance', views.vendor_performance, name='vendor-performance'),
]