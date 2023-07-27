from ..utils.setup import APITestSetup 
from django.urls import reverse 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class AuthTestCase(APITestSetup):
    
    def setUp(self) -> None:
        self.user1 = self.create_test_user()
        self.user2 = self.create_test_superuser()
        return super().setUp()
    
    def test_user_sign_up(self):
        url = reverse("authentication:create-account")
        user_data = {
            "first_name": "Patrick",
            "last_name": "Onyeogo",
            "email": "patrickonyeogo@gmail.com",
            "gender": "Male",
            "password": "Akpororo1",
            "password2": "Akpororo1"
        }
        res = self.client.post(url, user_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['status'], "Successful")
        
    def test_login_unverified_user(self):
        login_data = {
            "email": "kerryonyeogo@gmail.com",
            "password": "Akpororo1"
        }
        res = self.client.post(reverse("authentication:login"), login_data)
        # test to see if the user cannot login due to unverification
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)  
        
    def test_login_verified_user(self):
        login_data = {
            "email": "kerryonyeogo2@gmail.com",
            "password": "Akpororo1"
        }
        res = self.client.post(reverse("authentication:login"), login_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_refresh_token(self):
        url = reverse('authentication:token_refresh')
        data = {
            "refresh": str(RefreshToken.for_user(self.user2))
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_reset_password_request(self):
        url = reverse('authentication:reset-password-request-list')
        data = {
            "email": "kerryonyeogo@gmail.com"
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_forgot_password_request(self):
        url = reverse('authentication:forgot-password-request-list')
        data = {
            "email": "kerryonyeogo@gmail.com"
        }
        res = self.client.post(url, data)
        self.assertTrue(res.status_code, status.HTTP_200_OK)
        

        
        
    
        
    
