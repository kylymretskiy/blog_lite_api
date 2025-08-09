from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, SubPost
from .serializers import PostSerializer, PostDetailSerializer, SubPostSerializer, SubPostDetailSerializer
from django.db.models import F
from rest_framework.pagination import PageNumberPagination


@api_view(['POST'])
def like_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    post.likes_count = 1 if post.likes_count == 0 else 0
    post.save()
    return Response({"likes_count": post.likes_count}, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    post.views_count = F('views_count') + 1
    post.save(update_fields=['views_count'])
    post.refresh_from_db(fields=['views_count'])

    return Response({"views_count": post.views_count}, status=status.HTTP_200_OK)

@api_view(['GET','PUT','PATCH','DELETE'])
def post_detail_api_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Post does not exist'})
    if request.method == 'GET':
        data = PostDetailSerializer(post).data
        return Response(data=data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.method == 'PUT':
            post.title = request.data.get('title')
            post.body = request.data.get('body')
            post.author_id = request.data.get('author_id')
        else:
            if 'title' in request.data:
                post.title = request.data.get('title')
            if 'body' in request.data:
                post.body = request.data.get('body')
            if 'author_id' in request.data:
                post.author_id = request.data.get('author_id')
        post.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=PostDetailSerializer(post).data)
    else:
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def post_list_api_view(request):
    if request.method == 'GET':
        posts = Post.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 3

        result_page = paginator.paginate_queryset(posts, request)
        data = PostSerializer(result_page, many=True).data
        return paginator.get_paginated_response(data)

    elif request.method == 'POST':
        if isinstance(request.data, list):
            serializer = PostSerializer(data=request.data, many=True)
            if serializer.is_valid():
                posts_to_create = [Post(**item) for item in serializer.validated_data]
                Post.objects.bulk_create(posts_to_create)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                post = serializer.save()
                return Response(PostDetailSerializer(post).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','PATCH','DELETE'])
def subpost_detail_api_view(request, id):
    try:
        subpost = SubPost.objects.get(id=id)
    except SubPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'SubPost does not exist'})
    if request.method == 'GET':
        data = SubPostDetailSerializer(subpost).data
        return Response(data=data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.method == 'PUT':
            subpost.title = request.data.get('title')
            subpost.body = request.data.get('body')
            subpost.post_id = request.data.get('post_id')
        else:
            if 'title' in request.data:
                subpost.title = request.data.get('title')
            if 'body' in request.data:
                subpost.body = request.data.get('body')
            if 'post' in request.data:
                subpost.post_id = request.data.get('post')
        subpost.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=SubPostDetailSerializer(subpost).data)
    else:
        subpost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def subpost_list_api_view(request):
    if request.method == 'GET':
        subposts = SubPost.objects.all()
        data = SubPostSerializer(subposts,many=True).data
        return Response(data=data,
                        status=status.HTTP_200_OK)
    elif request.method == 'POST':
        title = request.data.get('title')
        body = request.data.get('body')
        post_id = request.data.get('post_id')
        subpost = SubPost.objects.create(
            title=title,
            body=body,
            post_id=post_id
        )
        return Response(status=status.HTTP_201_CREATED,
                        data=SubPostDetailSerializer(subpost).data)