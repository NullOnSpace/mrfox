from django.test import TestCase
from django.shortcuts import reverse

from .models import Author

# Create your tests here.
class AuthTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser = Author.objects.create_user('test',
            email='test@gmail.com', password='test123456')

    def test_user_auth(self):
        auth_url = reverse("account:auth")
        res = self.client.get(auth_url)
        self.assertEqual(res.status_code, 403)
        self.client.login(username='test', password="test123456")
        res = self.client.get(auth_url)
        self.assertEqual(res.status_code, 200)
