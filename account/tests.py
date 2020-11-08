from django.test import TestCase
from django.shortcuts import reverse
from django.conf import settings

from .models import Author

# Create your tests here.
class AuthTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser = Author.objects.create_user('test',
            email='test@gmail.com', password='test123456')

    def test_user_auth(self):
        # an anonymous user request auth will get 403
        auth_url = reverse("account:auth")
        res = self.client.get(auth_url)
        self.assertEqual(res.status_code, 403)
        # an authenticated user request auth will get 200
        self.client.login(username='test', password="test123456")
        res = self.client.get(auth_url)
        self.assertEqual(res.status_code, 200)
        # an user logout request auth will get 403
        # and will be redirect to LOGOUT_REDIRECT_URL
        logout_url = reverse("account:logout")
        res = self.client.get(logout_url)
        logout_redirect = settings.LOGOUT_REDIRECT_URL
        self.assertEqual(res.url, logout_redirect)
        res = self.client.get(auth_url)
        self.assertEqual(res.status_code, 403)
