from vendor.models import Vendor 
from ..utils.setup import APITestSetup 
import datetime 
from django.urls import reverse 
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
from vendor.serializers import VendorSerializer

class VendorAPITestCase(APITestSetup):
    
    def setUp(self):
        self.super_user = self.create_test_superuser()
        self.verified_user = self.create_test_verified_user()
        vendor_serializer = VendorSerializer(data={
            'bio': 'bio',
            'date_of_birth': datetime.datetime.today().date()
        })
        vendor_serializer.is_valid(raise_exception=True)
        self.vendor = vendor_serializer.save(user=self.super_user)
        
        refresh = RefreshToken.for_user(self.verified_user)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        return super().setUp()
    
    def test_vendor_creation(self):
        data = {
            'bio': "Gadget Vendor",
            'date_of_birth': datetime.date(year=2000, month=9, day=20),
        }
        res = self.client.post(path=reverse('create-vendor'), data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
    def test_vendor_creation_non_unique(self):
        # get authentication
        refresh = RefreshToken.for_user(self.super_user)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        
        data = {
            'bio': "Gadget Vendor",
            'date_of_birth': datetime.date(year=2000, month=9, day=20),
        }
        res = self.client.post(path=reverse('create-vendor'), data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_get_vendors_list(self):
        res = self.client.get(path=reverse('vendors-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_update_vendor_profile(self):
        # create the vendor profile
        vendor_serializer = VendorSerializer(data={
            'bio': 'bio',
            'date_of_birth': datetime.datetime.today().date()
        })
        vendor_serializer.is_valid(raise_exception=True)
        vendor = vendor_serializer.save(user=self.verified_user)
        # update the data
        update_data = {
            'bio': 'Phone Vendor Updated',
            'date_of_birth': datetime.date(year=2002, month=10, day=21)
        }
        res = self.client.put(path=reverse('vendor-detail', args=[vendor.pk]), data=update_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_retrieve_vendor_details(self):
        res = self.client.get(path=reverse('vendor-detail', args=[self.vendor.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_partial_update_vendor_details(self):
        # create the vendor profile
        vendor_serializer = VendorSerializer(data={
            'bio': 'bio',
            'date_of_birth': datetime.datetime.today().date()
        })
        vendor_serializer.is_valid(raise_exception=True)
        vendor = vendor_serializer.save(user=self.verified_user)
        # update the data
        update_data = {
            'bio': 'Phone Vendor Partial Updated',
        }
        res = self.client.put(path=reverse('vendor-detail', args=[vendor.pk]), data=update_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_delete_vendor_profile(self):
        vendor_serializer = VendorSerializer(data={
            'bio': 'bio',
            'date_of_birth': datetime.datetime.today().date()
        })
        vendor_serializer.is_valid(raise_exception=True)
        vendor = vendor_serializer.save(user=self.verified_user)
        res = self.client.delete(path=reverse('vendor-detail', args=[vendor.pk]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        