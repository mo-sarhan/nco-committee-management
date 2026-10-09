from django.test import TestCase,Client
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import PhotoInfo

# Create your tests here.


class PhotoTestCase(APITestCase):
    def test_photo_in_stock(self):
        url = reverse('upload-images')
        client = Client()
        respone = client.get(url)
        

        self.assertEqual(respone.status_code,status.HTTP_200_OK,'something when wrong')