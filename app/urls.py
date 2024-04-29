# vendor_management/urls.py

from django.urls import path
from .views import (
    VendorListCreateAPIView, VendorRetrieveUpdateDestroyAPIView,
    PurchaseOrderListCreateAPIView, PurchaseOrderRetrieveUpdateDestroyAPIView,VendorPerformanceAPIView,AcknowledgePurchaseOrderAPIView
)

urlpatterns = [
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-detail'),
    path('purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-detail'),
    path('vendors/performance/<int:vendor_id>/',VendorPerformanceAPIView.as_view() ,name="vendor-performance"),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge-purchase-order'),
]
