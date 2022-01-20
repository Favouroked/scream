from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, Like
from posts.serializers import PostSerializer


# Create your views here.
class PostAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def post(self, request):
        data = request.data
        post = Post.objects.create(user=request.user, text=data['text'])
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)
        return Response({**serializer.data, 'likes': post.likes}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_post_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get_object(self, user, post):
        try:
            return Like.objects.get(user=user, post=post)
        except Like.DoesNotExist:
            raise Http404

    def get(self, request, post_id):
        post = self.get_post_object(post_id)
        Like.objects.get_or_create(user=request.user, post=post)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        post = self.get_post_object(post_id)
        like = self.get_object(request.user, post)
        like.delete()
        return Response(status=status.HTTP_200_OK)
