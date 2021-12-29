from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Hospital.views import  HospitalLogin, HospitalRegister, HospitalMain, MapDistanceCalculate 

class TestUrls(SimpleTestCase):

    def test_HospitalLogin_url_is_resolved(self):
        url = reverse('HospitalLogin')
        self.assertEquals(resolve(url).func, HospitalLogin)
    
    def test_HospitalRegister_url_is_resolved(self):
        url = reverse('HospitalRegister')
        self.assertEquals(resolve(url).func, HospitalRegister)

    def test_HospitalMain_url_is_resolved(self):
        url = reverse('HospitalMain')
        self.assertEquals(resolve(url).func, HospitalMain)
        
    def test_MapDistanceCalculate_url_is_resolved(self):
        url = reverse('MapDistanceCalculate')
        self.assertEquals(resolve(url).func, MapDistanceCalculate)