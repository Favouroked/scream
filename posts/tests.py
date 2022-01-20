from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from posts.models import Post, Like
from users.models import User


def create_user():
    test_email = 'test@gmail.com'
    test_password = 'testCore`83'
    return User.objects.create_user(test_email, test_password)


def get_api_client():
    user = create_user()
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


# Create your tests here.
class PostsTests(APITestCase):

    def test_create_post(self):
        url = reverse('posts:index')
        client, _ = get_api_client()
        response = client.post(url, {'text': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['text'], 'Test')
        self.assertIsNotNone(response.data['created_at'])

    def test_get_post_by_id(self):
        client, user = get_api_client()
        post = Post.objects.create(user=user, text='Hi')
        url = reverse('posts:details', args=(post.id,))
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], post.id)
        self.assertEqual(response.data['text'], post.text)
        self.assertIsNotNone(response.data['created_at'])

    def test_update_post(self):
        client, user = get_api_client()
        test_post = Post.objects.create(user=user, text='Test')
        url = reverse('posts:details', args=(test_post.id,))
        response = client.put(url, {'text': 'Test1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], test_post.id)
        self.assertEqual(response.data['text'], 'Test1')
        self.assertIsNotNone(response.data['created_at'])
        post = Post.objects.get(id=test_post.id)
        self.assertEqual(post.text, 'Test1')

    def test_delete_post(self):
        client, user = get_api_client()
        post = Post.objects.create(user=user, text='Test')
        url = reverse('posts:details', args=(post.id,))
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        posts = Post.objects.filter(id=post.id)
        self.assertEqual(len(posts), 0)


class LikesTests(APITestCase):

    def test_like_post(self):
        client, user = get_api_client()
        post = Post.objects.create(user=user, text='Test')
        url = reverse('posts:like', args=(post.id,))
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        likes = Like.objects.filter(user=user, post=post)
        self.assertEqual(len(likes), 1)

    def test_unlike_post(self):
        client, user = get_api_client()
        post = Post.objects.create(user=user, text='Test')
        Like.objects.create(user=user, post=post)
        url = reverse('posts:like', args=(post.id,))
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        likes = Like.objects.filter(user=user, post=post)
        self.assertEqual(len(likes), 0)
