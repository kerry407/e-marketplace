from authentication.models import CustomUser
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
        
        
    
        
     
        
