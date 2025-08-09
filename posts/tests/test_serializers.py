from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post, SubPost
from posts.serializers import PostSerializer, PostDetailSerializer, SubPostSerializer, SubPostDetailSerializer

class SerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Title', body='Body', author=self.user)
        self.subpost = SubPost.objects.create(title='SubTitle', body='SubBody', post=self.post)

    def test_post_serializer(self):
        serializer = PostSerializer(self.post)
        data = serializer.data
        self.assertEqual(data['title'], self.post.title)
        self.assertEqual(data['author_id'], self.user.id)
        self.assertIsInstance(data['subposts'], list)

    def test_post_detail_serializer(self):
        serializer = PostDetailSerializer(self.post)
        data = serializer.data
        self.assertIn('subpost_list', data)
        self.assertEqual(data['title'], self.post.title)

    def test_subpost_serializer(self):
        serializer = SubPostSerializer(self.subpost)
        data = serializer.data
        self.assertEqual(data['title'], self.subpost.title)

    def test_subpost_detail_serializer(self):
        serializer = SubPostDetailSerializer(self.subpost)
        data = serializer.data
        self.assertEqual(data['title'], self.subpost.title)
