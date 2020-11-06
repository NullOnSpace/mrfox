from django.test import TestCase, Client
from django.shortcuts import reverse

# Create your tests here.
class AnonymousTest(TestCase):
    fixtures = []

    def test_anonymous_user_cant_create_post(self):
        create_url = reverse('blog:post_create')
        res = self.client.post(create_url, {
            'title': 'dummy post by anonymous',
            'body': 'dummy post by anonymous',
            'status': 'published',
        })
        login_url = reverse('account:login')
        self.assertEqual(res.url, login_url+"?next="+create_url)
