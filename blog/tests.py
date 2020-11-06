from django.test import TestCase, Client
from django.shortcuts import reverse

from .models import Post
from account.models import Author

# Create your tests here.
class AnonymousTest(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(self):
        user = Author.objects.get(pk=3)
        self.post = Post.objects.create(
            title='post by test1',
            body='post by test1',
            status='published',
            author=user,
        )

    def setUp(self):
        self.post.refresh_from_db()

    def test_anonymous_user_cant_create_post(self):
        create_url = reverse('blog:post_create')
        post_count = Post.objects.count()
        res = self.client.post(create_url, {
            'title': 'dummy post by anonymous',
            'body': 'dummy post by anonymous',
            'status': 'published',
        })
        login_url = reverse('account:login')
        self.assertEqual(res.url, login_url+"?next="+create_url)
        post_count_new = Post.objects.count()
        self.assertEqual(post_count, post_count_new)

    def test_anonymous_user_cant_update_post(self):
        update_url = reverse('blog:post_edit', kwargs={'pk': self.post.pk})
        updated_post = {
            'title': 'post edit by anony',
            'body': 'post edit by anony',
            'status': 'published',
        }
        res = self.client.post(update_url, updated_post)
        login_url = reverse('account:login')
        self.assertEqual(res.url, login_url+"?next="+update_url)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, updated_post['title'])
        self.assertNotEqual(self.post.body, updated_post['body'])

    def test_anonymous_user_cant_delete_post(self):
        delete_url = reverse('blog:post_del', kwargs={'pk': self.post.pk})
        post_count = Post.objects.count()
        res = self.client.post(delete_url)
        login_url = reverse('account:login')
        self.assertEqual(res.url, login_url+"?next="+delete_url)
        post_count_new = Post.objects.count()
        self.assertEqual(post_count, post_count_new)

    def test_anonymous_user_can_access_post(self):
        access_url = reverse('blog:post_detail', kwargs={"pk": self.post.pk})
        res = self.client.get(access_url)
        self.assertIn(b'post by test1', res.content)


class SingleUserTest(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(self):
        self.user = Author.objects.get(pk=3)
        self.user2 = Author.objects.get(pk=4)
        self.post = Post.objects.create(
            title='post by test1',
            body='post by test1',
            status='published',
            author=self.user,
        )
        self.post2 = Post.objects.create(
            title='post by test2',
            body='post by test2',
            status='published',
            author=self.user2,
        )

    def setUp(self):
        self.post.refresh_from_db()
        self.client.force_login(self.user)

    def test_single_user_access_self_post(self):
        kwargs = {"pk": self.post.pk}
        access_url = reverse('blog:post_detail', kwargs=kwargs)
        res = self.client.get(access_url)
        self.assertIn(b'post by test1', res.content)
        # edit links are in self's post page
        edit_url = reverse('blog:post_edit', kwargs=kwargs)
        self.assertIn(edit_url.encode("utf8"), res.content)
        delete_url = reverse('blog:post_del', kwargs=kwargs)
        self.assertIn(delete_url.encode("utf8"), res.content)

    def test_single_user_can_create_post(self):
        create_url = reverse('blog:post_create')
        post_count = Post.objects.count()
        res = self.client.post(create_url, {
            'title': 'new post created by user1',
            'body': 'new post created by user1',
            'status': 'published',
        })
        new_post = Post.objects.get(title='new post created by user1')
        new_post_url = new_post.get_absolute_url()
        # after creating, jump to detail page
        self.assertEqual(res.url, new_post_url)
        self.assertEqual(new_post.author, self.user)

    def test_single_user_can_update_self_post(self):
        update_url = reverse('blog:post_edit', kwargs={'pk': self.post.pk})
        updated_post = {
            'title': 'post edited by user1',
            'body': 'post edited by user1',
            'status': 'published',
        }
        res = self.client.post(update_url, updated_post)
        self.post.refresh_from_db()
        self.assertEqual(self.post.get_absolute_url(), res.url)
        self.assertEqual(self.post.title, updated_post['title'])
        self.assertEqual(self.post.body, updated_post['body'])

    def test_single_user_can_delete_self_post(self):
        delete_url = reverse('blog:post_del', kwargs={'pk': self.post.pk})
        post_count = Post.objects.count()
        res = self.client.post(delete_url)
        post_list_url = reverse('blog:post_list')
        self.assertEqual(res.url, post_list_url)
        post_count_new = Post.objects.count()
        self.assertEqual(post_count, post_count_new+1)

    def test_single_user_access_others_post(self):
        kwargs = {"pk": self.post2.pk}
        access_url = reverse('blog:post_detail', kwargs=kwargs)
        res = self.client.get(access_url)
        self.assertIn(b'post by test2', res.content)
        # edit links are not in other's post page
        edit_url = reverse('blog:post_edit', kwargs=kwargs)
        self.assertNotIn(edit_url.encode("utf8"), res.content)
        delete_url = reverse('blog:post_del', kwargs=kwargs)
        self.assertNotIn(delete_url.encode("utf8"), res.content)

    def test_single_user_cant_update_others_post(self):
        update_url = reverse('blog:post_edit', kwargs={'pk': self.post2.pk})
        updated_post = {
            'title': 'post edit by user1',
            'body': 'post edit by user1',
            'status': 'published',
        }
        res = self.client.post(update_url, updated_post)
        self.assertEqual(res.status_code, 403)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, updated_post['title'])
        self.assertNotEqual(self.post.body, updated_post['body'])

    def test_single_user_cant_delete_others_post(self):
        delete_url = reverse('blog:post_del', kwargs={'pk': self.post2.pk})
        post_count = Post.objects.count()
        res = self.client.post(delete_url)
        self.assertEqual(res.status_code, 403)
        post_count_new = Post.objects.count()
        self.assertEqual(post_count, post_count_new)
