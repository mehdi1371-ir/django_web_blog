from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='user1')
        cls.post1 = Post.objects.create(
            title='post1',
            text='post1 description',
            status=Post.STATUS_CHOICES[0][0],
            author=cls.user
        )
        cls.post2 = Post.objects.create(
            title='post2',
            text='post2 description',
            status=Post.STATUS_CHOICES[1][0],
            author=cls.user
        )

    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_objects_entrance(self):
        self.assertEqual(self.post1.title, 'post1')
        self.assertEqual(self.post1.text, 'post1 description')
        self.assertEqual(self.post1.status, Post.STATUS_CHOICES[0][0])
        self.assertEqual(self.post1.author, self.user)

    def test_home_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_post_details_on_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)
        self.assertContains(response, self.post1.author)

    def test_post_detail_url(self):
        response = self.client.get(f'/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_details_on_detail_page(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)
        self.assertContains(response, self.post1.author)

    def test_status_404_if_post_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_in_home(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, self.post2.title)

    def test_draft_not_show_in_details(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'some title',
            'text': 'some text',
            'status': 'pub',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)  # redirection test
        self.assertEqual(Post.objects.last().title, 'some title')
        self.assertEqual(Post.objects.last().text, 'some text')
        self.assertEqual(Post.objects.last().status, 'pub')
        self.assertEqual(Post.objects.last().author, self.user)

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'post2 updated',
            'text': 'this text is updated',
            'status': 'drf',
            'author': self.post1.author.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'post2 updated')
        self.assertEqual(Post.objects.last().text, 'this text is updated')
        self.assertEqual(Post.objects.last().author, self.post1.author)

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post1.id]))
        self.assertEqual(response.status_code, 302)

