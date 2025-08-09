from rest_framework import serializers
from .models import Post, SubPost


class SubPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPost
        fields = '__all__'

class SubPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPost
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    subposts = SubPostSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id' , 'title', 'body', 'author_id', 'created_at', 'updated_at', 'subposts']


class PostDetailSerializer(serializers.ModelSerializer):
    subpost_list = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = 'id title body author_id created_at updated_at subpost_list'.split()

    def get_subpost_list(self, post):
        return SubPostSerializer(post.subposts.all(), many=True).data
