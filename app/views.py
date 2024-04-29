from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from rest_framework.permissions import IsAuthenticated

from .view_ext import calculate_average_response_time,calculate_fulfilment_rate,calculate_on_time_delivery_rate,calculate_quality_rating_average

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]


class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

class VendorPerformanceAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'vendor_id'

    def retrieve (self, request, *args, **kwargs):
        vendor = self.get_object()
        performance_data = {
            'on_time_delivery_rate': calculate_on_time_delivery_rate(vendor),
            'quality_rating_avg': calculate_quality_rating_average(vendor),
            'average_response_time': calculate_average_response_time(vendor),
            'fulfillment_rate': calculate_fulfilment_rate(vendor)
        }
        return Response(performance_data)

    
class AcknowledgePurchaseOrderAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    lookup_url_kwarg = 'po_id'
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        purchase_order = self.get_object()
        purchase_order.acknowledge()
        return Response(status=status.HTTP_200_OK)