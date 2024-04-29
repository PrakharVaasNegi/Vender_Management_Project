from django.db.models import Count, F, ExpressionWrapper, fields
from .models import PurchaseOrder



def calculate_on_time_delivery_rate(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed')
    on_time_pos = completed_pos.filter(delivery_date__lte=F('acknowledgment_date'))
    total_completed_pos = completed_pos.count()
    if total_completed_pos > 0:
        return on_time_pos.count() / total_completed_pos
    else:
        return 0.0

    
def calculate_quality_rating_average(vendor):
    completed_pos_with_ratings = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
    if completed_pos_with_ratings.exists():
        avg_ratings = completed_pos_with_ratings.aggregate(avg_ratings=Avg('quality_rating'))['avg_ratings']
        return avg_ratings
    else:
        return 0.0

from django.db.models import Avg, ExpressionWrapper, fields

def calculate_average_response_time(vendor):
    completed_pos_with_acknowledgment = vendor.purchaseorder_set.filter(
        status='completed', acknowledgment_date__isnull=False
    )
    total_completed_pos = completed_pos_with_acknowledgment.count()
    if total_completed_pos > 0:
        avg_response_time = completed_pos_with_acknowledgment.aggregate(
            avg_response_time=Avg(F('acknowledgment_date') - F('issue_date'))
        )['avg_response_time']
        if avg_response_time is not None:
            return avg_response_time.total_seconds() / 3600  # Convert to hours
    return 0.0


def calculate_fulfilment_rate(vendor):
    total_pos = vendor.purchaseorder_set.count()
    if total_pos > 0:
        fulfilled_pos = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=True)
        return fulfilled_pos.count() / total_pos
    return 0.0


