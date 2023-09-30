from datetime import datetime 
from vendor.models import Vendor, Store 
from ..utils.setup import TestSetup
from vendor.serializers import VendorSerializer, StoreSerializer



class VendorModelTestCase(TestSetup):
    
    def setUp(self) -> None:
        vendor_serializer = VendorSerializer(data={
            'bio': 'bio',
            'date_of_birth': datetime.today().date()
        })
        vendor_serializer.is_valid(raise_exception=True)
        self.vendor = vendor_serializer.save(user=self.create_test_superuser())
        return super().setUp()
    
    def test_vendor_model(self):
        self.assertTrue(isinstance(self.vendor, Vendor))
        self.assertTrue(self.vendor.user.is_verified)
        self.assertTrue(self.vendor.user.is_vendor)
        self.assertEqual(self.vendor.bio, 'bio')
        
        
class StoreModelTestCase(TestSetup):
    
    def setUp(self) -> None:
        vendor_serializer = VendorSerializer(data={
            'bio': 'bio',
            'date_of_birth': datetime.today().date()
        })
        vendor_serializer.is_valid(raise_exception=True)
        vendor = vendor_serializer.save(user=self.create_test_superuser())
        store_serializer = StoreSerializer(data={
            'name':'Alfred Gardens',
            'description':'Flower Store'
        })
        store_serializer.is_valid(raise_exception=True)
        self.store = store_serializer.save(owner=vendor)
        return super().setUp()
        
    def test_store_model(self):
        self.assertTrue(isinstance(self.store, Store))
        self.assertTrue(self.store.owner.user.is_verified)
        self.assertTrue(self.store.owner.user.is_vendor)