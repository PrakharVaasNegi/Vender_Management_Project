from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from .view_ext import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_average,
    calculate_average_response_time,
    calculate_fulfilment_rate,
)

# Signal to recalculate metrics when Purchase Order is saved
@receiver(post_save, sender=PurchaseOrder)
def update_metrics(sender, instance, **kwargs):
    print('---------------------------WORKING------------------------')
    print('---------------------------WORKING------------------------')
    print('---------------------------WORKING------------------------')
    vendor = instance.vendor
    vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    vendor.quality_rating_avg = calculate_quality_rating_average(vendor)
    vendor.average_response_time = calculate_average_response_time(vendor)
    vendor.fulfillment_rate = calculate_fulfilment_rate(vendor)
    vendor.save()
