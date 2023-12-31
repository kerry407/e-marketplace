from vendor.models import Vendor, Store, StoreSetting
from ..utils.setup import APITestSetup 
import datetime 
from django.urls import reverse 
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
from vendor.serializers import VendorSerializer, StoreSerializer

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
        user = res.json()['data']['user']
        vendor = Vendor.objects.get(user=user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(vendor.user.is_vendor)
        
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
        self.assertTrue(vendor.user.is_vendor)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_retrieve_vendor_details(self):
        res = self.client.get(path=reverse('vendor-detail', args=[self.vendor.pk]))
        self.assertTrue(self.vendor.user.is_vendor)
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
        self.assertTrue(vendor.user.is_vendor)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_delete_vendor_profile(self):
        vendor_serializer = VendorSerializer(data={
            'bio': 'bio',
            'date_of_birth': datetime.datetime.today().date()
        })
        vendor_serializer.is_valid(raise_exception=True)
        vendor = vendor_serializer.save(user=self.verified_user)
        res = self.client.delete(path=reverse('vendor-detail', args=[vendor.pk]))
        self.assertTrue(vendor.user.is_vendor)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class StoreAPITestCase(APITestSetup):
    
    def setUp(self):
        self.super_user = self.create_test_superuser()
        self.verified_user = self.create_test_verified_user()
        vendor_serializer = VendorSerializer(data={
            'bio': 'bio',
            'date_of_birth': datetime.datetime.today().date()
        })
        vendor_serializer.is_valid(raise_exception=True)
        self.vendor = vendor_serializer.save(user=self.verified_user)
        store_serializer = StoreSerializer(data={
            'name': 'Gadgetify',
            'description': 'Gadget Store'
        })
        store_serializer.is_valid(raise_exception=True)
        self.store = store_serializer.save(owner=self.vendor)
        
        refresh = RefreshToken.for_user(self.verified_user)
        access_token = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION= f"Bearer {access_token}")
        return super().setUp()
    
    def test_store_creation(self):
        data = {
            'name':'iconnect',
            'description':'gadget store'
        }
        res = self.client.post(path=reverse('create-store'), data=data)
        settings = StoreSetting.objects.filter(store__name='iconnect')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(settings.exists())
        
    def test_store_creation_non_unique(self):
        data = {
            'name':'Gadgetify',
            'description':'gadget store'
        }
        res = self.client.post(path=reverse('create-store'), data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_store_list(self):
        res = self.client.get(path=reverse('store-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_retrieve_store_detail(self):
        res = self.client.get(path=reverse('store-detail', args=[self.store.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_update_store_detail(self):
        data = {
            'name': 'iGadget',
            'description': "One stop shop for all your gadgets"
        }
        res = self.client.put(path=reverse('store-detail', args=[self.store.pk]), data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        

    def test_partial_update_store_detail(self):
        data = {
            'name': 'iGadget',
        }
        res = self.client.patch(path=reverse('store-detail', args=[self.store.pk]), data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_update_store_non_unique(self):
        # create a new store with a different name
        store_serializer = StoreSerializer(data={
            'name': 'SP Gadgets',
            'description': 'Gadget Store'
        })
        store_serializer.is_valid(raise_exception=True)
        store = store_serializer.save(owner=self.vendor)
        # use the same name as created before to test update
        data = {
            'name': 'Gadgetify',
            'description': "One stop shop for all your gadgets"
        }
        res = self.client.patch(path=reverse('store-detail', args=[store.pk]), data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_store(self):
        res = self.client.delete(path=reverse('store-detail', args=[self.store.pk]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)