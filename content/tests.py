from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from content.models import MediaContent

class MediaContentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.content_list_url = reverse('mediacontent-list')

        # Create a user for authentication
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='password123')
        self.admin_user = User.objects.create_superuser(email='admin@example.com', username='adminuser', password='adminpassword')

        # Get JWT token for the user
        login_data = {'email': 'test@example.com', 'password': 'password123'}
        response = self.client.post(reverse('token_obtain_pair'), login_data, format='json')
        self.access_token = response.data['access']

        # Get JWT token for the admin user
        admin_login_data = {'email': 'admin@example.com', 'password': 'adminpassword'}
        response = self.client.post(reverse('token_obtain_pair'), admin_login_data, format='json')
        self.admin_access_token = response.data['access']

    def test_create_media_content_authenticated(self):
        """
        Ensure an authenticated user can create media content.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        data = {
            'title': 'New Game Title',
            'description': 'A description for the new game.',
            'category': 'game',
            'content_url': 'http://example.com/newgame.zip'
        }
        response = self.client.post(self.content_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MediaContent.objects.count(), 1)
        self.assertEqual(MediaContent.objects.get().title, 'New Game Title')

    def test_create_media_content_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot create media content.
        """
        data = {
            'title': 'Unauthorized Content',
            'description': 'Should not be created.',
            'category': 'video',
            'content_url': 'http://example.com/unauth.mp4'
        }
        response = self.client.post(self.content_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MediaContent.objects.count(), 0)

    def test_list_media_content(self):
        """
        Ensure anyone can list media content.
        """
        MediaContent.objects.create(title='Game 1', description='Desc 1', category='game', content_url='http://example.com/game1.zip')
        MediaContent.objects.create(title='Video 1', description='Desc 2', category='video', content_url='http://example.com/video1.mp4')

        response = self.client.get(self.content_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) # Assuming pagination is enabled

    def test_retrieve_media_content(self):
        """
        Ensure anyone can retrieve a single media content item.
        """
        content = MediaContent.objects.create(title='Artwork 1', description='Desc 3', category='artwork', content_url='http://example.com/artwork1.jpg')
        detail_url = reverse('mediacontent-detail', kwargs={'pk': content.media_id})

        response = self.client.get(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Artwork 1')

    def test_update_media_content_authenticated(self):
        """
        Ensure an authenticated user can update their own media content.
        """
        content = MediaContent.objects.create(title='Old Title', description='Old Desc', category='music', content_url='http://example.com/old.mp3')
        detail_url = reverse('mediacontent-detail', kwargs={'pk': content.media_id})

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated Desc',
            'category': 'music',
            'content_url': 'http://example.com/updated.mp3'
        }
        response = self.client.put(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content.refresh_from_db()
        self.assertEqual(content.title, 'Updated Title')

    def test_delete_media_content_authenticated(self):
        """
        Ensure an authenticated user can delete their own media content.
        """
        content = MediaContent.objects.create(title='To Be Deleted', description='Delete me', category='game', content_url='http://example.com/delete.zip')
        detail_url = reverse('mediacontent-detail', kwargs={'pk': content.media_id})

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MediaContent.objects.count(), 0)

    def test_delete_media_content_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot delete media content.
        """
        content = MediaContent.objects.create(title='Protected Content', description='Keep me', category='video', content_url='http://example.com/protected.mp4')
        detail_url = reverse('mediacontent-detail', kwargs={'pk': content.media_id})

        response = self.client.delete(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MediaContent.objects.count(), 1)