from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from posts.models import Post, SubPost

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Test Post', body='Body', author=self.user)
        self.subpost = SubPost.objects.create(title='Test SubPost', body='Body', post=self.post)

    def test_get_post_list(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_post_detail(self):
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

    def test_like_post(self):
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('likes_count', response.data)

    def test_view_post(self):
        response = self.client.get(f'/api/posts/{self.post.id}/view/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('views_count', response.data)

    def test_get_subpost_list(self):
        response = self.client.get('/api/subposts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_subpost_detail(self):
        response = self.client.get(f'/api/subposts/{self.subpost.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.subpost.title)

    def test_post_create(self):
        data = {'title': 'New Post', 'body': 'New Body', 'author_id': self.user.id}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Post')

    def test_subpost_create(self):
        data = {'title': 'New SubPost', 'body': 'New Body', 'post_id': self.post.id}
        response = self.client.post('/api/subposts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New SubPost')
