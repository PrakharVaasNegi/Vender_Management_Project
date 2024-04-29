from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Vendor, PurchaseOrder

class APITest(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a token for the user
        self.token = Token.objects.create(user=self.user)
        # Set token in the authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create some initial data for testing
        self.vendor1 = Vendor.objects.create(name='Vendor 1', contact_details='Contact 1', address='Address 1', vendor_code='V001')
        self.vendor2 = Vendor.objects.create(name='Vendor 2', contact_details='Contact 2', address='Address 2', vendor_code='V002')

        self.purchase_order1 = PurchaseOrder.objects.create(vendor=self.vendor1, po_number='PO001', order_date='2024-04-30', delivery_date='2024-05-10', items={}, quantity=10, status='completed', issue_date='2024-04-30', acknowledgment_date='2024-05-01')
        self.purchase_order2 = PurchaseOrder.objects.create(vendor=self.vendor2, po_number='PO002', order_date='2024-04-30', delivery_date='2024-05-12', items={}, quantity=15, status='completed', issue_date='2024-04-30', acknowledgment_date='2024-05-02')

    def test_vendor_list_create_api(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'name': 'New Vendor',
            'contact_details': 'New Contact',
            'address': 'New Address',
            'vendor_code': 'V003'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 3)

    def test_vendor_performance_api(self):
        url = reverse('vendor-performance', kwargs={'vendor_id': self.vendor1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions as needed

    def test_acknowledge_purchase_order_api(self):
        url = reverse('acknowledge-purchase-order', kwargs={'po_id': self.purchase_order1.id})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions as needed

# Add more test cases as needed
