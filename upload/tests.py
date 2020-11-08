from django.test import TestCase
from django.urls import reverse

from account.models import Author

# Create your tests here.
class UploadFileTest(TestCase):
    def test_upload_file(self):
        user = Author.objects.create_user(
            username="test", password='test123456', email="test@gmail.com",
        )
        self.client.force_login(user)
        upload_url = reverse('upload:upload')
        success_url = reverse('blog:post_list')
        with open("README.md", "rb") as fp:
            res = self.client.post(
                upload_url,
                data={'file': fp})
        self.assertEqual(res.url, success_url)
        # Anonymous user cant upload
        self.client.logout()
        with open("README.md", "rb") as fp:
            res = self.client.post(
                upload_url,
                data={'file': fp})
        self.assertNotEqual(res.url, success_url)
