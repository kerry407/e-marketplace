from datetime import datetime 
from vendor.models import Vendor 
from ..utils.setup import TestSetup



class VendorModelTestCase(TestSetup):
    
    def setUp(self) -> None:
        self.vendor = Vendor.objects.create(
                                            user=self.create_test_superuser(), 
                                            bio="bio",
                                            date_of_birth=datetime.today().date()
                                            )
        return super().setUp()
    
    def test_vendor_model(self):
        self.assertTrue(isinstance(self.vendor, Vendor))
        self.assertTrue(self.vendor.user.is_verified)
        self.assertEqual(self.vendor.bio, 'bio')