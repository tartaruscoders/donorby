from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from Hospital.models import  Measurement
from Hospital.views import  HospitalLogin, HospitalRegister, HospitalMain, MapDistanceCalculate 
import json
from django.contrib.auth import get_user_model

User = get_user_model()

class TestViews(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.HospitalLogin_url = reverse('HospitalLogin')
        # print(reverse('HospitalLogin'))
        user_a = User(username='test_account', email='test@example.com')
        user_a_pw = ('@test_password')
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a
        
    def test_HospitalLogin_POST_login_in_user(self):
        response = self.client.post(self.HospitalLogin_url,{'username' : 'test_account', 'password': '@test_password'}, follow=True)
        status_code = response.status_code
        print(status_code)
        # self.assertEqual(status_code, 200)
