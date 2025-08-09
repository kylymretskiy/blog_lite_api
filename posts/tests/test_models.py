from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post, SubPost

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Title', body='Body', author=self.user)

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Title')

class SubPostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Title', body='Body', author=self.user)
        self.subpost = SubPost.objects.create(title='SubTitle', body='SubBody', post=self.post)

    def test_subpost_str(self):
        self.assertEqual(str(self.subpost), 'SubTitle')
