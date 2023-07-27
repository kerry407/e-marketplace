from datetime import datetime 
from authentication.models import CustomUser, Vendor
from ..utils.setup import TestSetup



class CustomUserModelTestCase(TestSetup):
    
    def test_custom_user_creation(self):
        user = self.create_test_user()
        self.assertTrue(isinstance(user, CustomUser))
        self.assertEqual(user.__str__(), user.get_user_fullname)
        self.assertFalse(user.is_verified)
        
    def test_custom_superuser_creation(self):
        user = self.create_test_superuser()
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_verified)
        
class VendorModelTestCase(TestSetup):
    
    def setUp(self) -> None:
        self.vendor = Vendor.objects.create(
                                            user=self.create_test_superuser(), 
                                            bio="bio",
                                            date_of_birth=datetime.today().date()
                                            )
        return super().setUp()
    
    def test_vendor_creation(self):
        self.assertTrue(isinstance(self.vendor, Vendor))
        self.assertTrue(self.vendor.user.is_verified)
        self.assertEqual(self.vendor.bio, 'bio')
        
    
        
     
        
