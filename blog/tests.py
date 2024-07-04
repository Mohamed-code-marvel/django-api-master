from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post, Comment

class BlogTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'Test Post', 'content': 'This is a test post.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')

    def test_update_post(self):
        post = Post.objects.create(author=self.user, title='Initial Title', content='Initial Content')
        url = reverse('post-detail', args=[post.id])
        updated_data = {'title': 'Updated Title', 'content': 'Updated Content'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Title')

    def test_delete_post(self):
        post = Post.objects.create(author=self.user, title='To be deleted', content='Delete this post.')
        url = reverse('post-detail', args=[post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_create_comment(self):
        post = Post.objects.create(author=self.user, title='Test Post', content='This is a test post.')
        url = reverse('comment-list')
        data = {'post': post.id, 'content': 'This is a test comment.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'This is a test comment.')



    def test_update_comment_invalid_data(self):
        # Create a post for the comment
        post = Post.objects.create(author=self.user, title='Test Post', content='This is a test post.')
        # Create a comment to be updated
        comment = Comment.objects.create(post=post, author=self.user, content='Initial comment.')
        url = reverse('comment-detail', args=[comment.id])
        invalid_data = {}
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Initial comment.')

    def test_update_comment_permission_denied(self):
        another_user = User.objects.create_user(
            username='anotheruser', password='testpassword')
        post = Post.objects.create(author=self.user, title='Test Post', content='This is a test post.')
        comment = Comment.objects.create(post=post, author=self.user, content='Initial comment.')
        self.client.force_authenticate(user=another_user)
        url = reverse('comment-detail', args=[comment.id])
        updated_data = {'content': 'Updated comment by another user.'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Initial comment.')
    


    def test_update_comment_empty_content(self):
        post = Post.objects.create(author=self.user, title='Test Post', content='This is a test post.')
        comment = Comment.objects.create(post=post, author=self.user, content='Initial comment.')
        url = reverse('comment-detail', args=[comment.id])
        updated_data = {'content': ''}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Initial comment.')

    def test_update_nonexistent_comment(self):
        post = Post.objects.create(author=self.user, title='Test Post', content='This is a test post.')
        url = reverse('comment-detail', args=[999]) 
        updated_data = {'content': 'Trying to update non-existent comment.'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_comment_author_not_logged_in(self):
        post = Post.objects.create(author=self.user, title='Test Post', content='This is a test post.')
        comment = Comment.objects.create(post=post, author=self.user, content='Initial comment.')
        self.client.logout()
        url = reverse('comment-detail', args=[comment.id])
        updated_data = {'content': 'Trying to update comment without login.'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Initial comment.')

    def test_update_comment_different_post_author(self):
        another_user = User.objects.create_user(
            username='anotheruser', password='testpassword')
        post = Post.objects.create(author=another_user, title='Another User Post', content='This is another user post.')
        comment = Comment.objects.create(post=post, author=another_user, content='Initial comment by another user.')
        url = reverse('comment-detail', args=[comment.id])
        updated_data = {'content': 'Trying to update another user\'s comment.'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Initial comment by another user.')


