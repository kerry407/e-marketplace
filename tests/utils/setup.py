from django.test import TestCase  
from django.contrib.auth import get_user_model 
from authentication.models import CustomUser
from rest_framework.test import APITestCase
from typing import Dict, Any 

User = get_user_model()


class TestSetup(TestCase):
    
    def setUp(self) -> None:
        print(f"Starting test for {str(self)}...")
        print("---------------")
        return super().setUp()
        
    def create_test_user(self, **kwargs: Dict[str, Any]) -> CustomUser:
        user = User.objects.create(
            email='kerryonyeogo@gmail.com', first_name='test',
            last_name='test&test', gender='Male', phone_number='+2348102012239',
            address='9 olarenwaju street', city='Ikeja', state='Lagos',
            country='NG', **kwargs
        )
        return user
    
    def create_test_superuser(self, **kwargs: Dict[str, Any]) -> CustomUser:
        user = User.objects.create_user(
            email='kerryonyeogo2@gmail.com', first_name='test',
            last_name='test&test', password="Akpororo1", gender='Male', phone_number='+2348102012239',
            address='9 olarenwaju street', city='Ikeja', state='Lagos',
            country='NG', is_superuser=True
        )
        return user
        
    
    def tearDown(self) -> None:
        print(f"Finished test for {str(self)}...")
        print("---------------")
        return super().tearDown()
        

class APITestSetup(APITestCase):
    
    def setUp(self) -> None:
        print(f"Starting test for {str(self)}...")
        print("---------------")
        return super().setUp()
    
    def create_test_user(self, **kwargs: Dict[str, Any]) -> CustomUser:
        user = User.objects.create_user(
            email='kerryonyeogo@gmail.com', first_name='test',
            last_name='test&test', password="Akpororo1", **kwargs
        )
        return user
    
    def create_test_superuser(self, **kwargs: Dict[str, Any]) -> CustomUser:
        user = User.objects.create_user(
            email='kerryonyeogo2@gmail.com', first_name='test',
            last_name='test&test', password="Akpororo1", is_superuser=True, 
            **kwargs
        )
        return user
    
    def tearDown(self) -> None:
        print(f"Finished test for {str(self)}...")
        print("---------------")
        return super().tearDown()
    
     
        
