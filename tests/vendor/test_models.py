from datetime import datetime 
from vendor.models import Vendor 
from ..utils.setup import TestSetup
from vendor.serializers import VendorSerializer



class VendorModelTestCase(TestSetup):
    
    def setUp(self) -> None:
        # self.vendor = Vendor.objects.create(
        #                                     user=self.create_test_superuser(), 
        #                                     bio="bio",
        #                                     date_of_birth=datetime.today().date()
        #                                     )
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
        self.assertEqual(self.vendor.bio, 'bio')