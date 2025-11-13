from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from content.models import MediaContent
from ratings.models import Rating

class RatingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rating_list_url = reverse('rating-list')

        # Create users
        self.user1 = User.objects.create_user(email='user1@example.com', username='user1', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', username='user2', password='password123')

        # Create media content
        self.media1 = MediaContent.objects.create(
            title='Test Game', description='A test game', category='game', content_url='http://test.com/game.zip'
        )
        self.media2 = MediaContent.objects.create(
            title='Test Video', description='A test video', category='video', content_url='http://test.com/video.mp4'
        )

        # Get JWT token for user1
        login_data1 = {'email': 'user1@example.com', 'password': 'password123'}
        response1 = self.client.post(reverse('token_obtain_pair'), login_data1, format='json')
        self.access_token1 = response1.data['access']

        # Get JWT token for user2
        login_data2 = {'email': 'user2@example.com', 'password': 'password123'}
        response2 = self.client.post(reverse('token_obtain_pair'), login_data2, format='json')
        self.access_token2 = response2.data['access']

    def test_create_rating_authenticated(self):
        """
        Ensure an authenticated user can create a rating.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token1)
        data = {
            'media_content': str(self.media1.media_id),
            'value': 5
        }
        response = self.client.post(self.rating_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get().user, self.user1)
        self.assertEqual(Rating.objects.get().media_content, self.media1)
        self.assertEqual(Rating.objects.get().value, 5)

    def test_create_rating_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot create a rating.
        """
        data = {
            'media_content': str(self.media1.media_id),
            'value': 3
        }
        response = self.client.post(self.rating_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Rating.objects.count(), 0)

    def test_user_cannot_rate_same_content_twice(self):
        """
        Ensure a user cannot rate the same media content more than once.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token1)
        data = {
            'media_content': str(self.media1.media_id),
            'value': 4
        }
        self.client.post(self.rating_list_url, data, format='json') # First rating
        response = self.client.post(self.rating_list_url, data, format='json') # Second rating
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'You have already rated this media content.')

    def test_list_ratings_by_media_content(self):
        """
        Ensure ratings can be filtered by media_content_id.
        """
        Rating.objects.create(user=self.user1, media_content=self.media1, value=5)
        Rating.objects.create(user=self.user2, media_content=self.media1, value=4)
        Rating.objects.create(user=self.user1, media_content=self.media2, value=3)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token1)
        response = self.client.get(self.rating_list_url, {'media_content_id': str(self.media1.media_id)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        for rating in response.data['results']:
            self.assertEqual(str(rating['media_content']), str(self.media1.media_id))

    def test_update_rating_authenticated_owner(self):
        """
        Ensure an authenticated user can update their own rating.
        """
        rating = Rating.objects.create(user=self.user1, media_content=self.media1, value=3)
        detail_url = reverse('rating-detail', kwargs={'pk': rating.rating_id})

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token1)
        updated_data = {
            'media_content': str(self.media1.media_id), # media_content is required even for partial update
            'value': 5
        }
        response = self.client.patch(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rating.refresh_from_db()
        self.assertEqual(rating.value, 5)

    def test_update_rating_authenticated_not_owner(self):
        """
        Ensure an authenticated user cannot update another user's rating.
        """
        rating = Rating.objects.create(user=self.user1, media_content=self.media1, value=3)
        detail_url = reverse('rating-detail', kwargs={'pk': rating.rating_id})

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token2) # User2 tries to update User1's rating
        updated_data = {
            'media_content': str(self.media1.media_id),
            'value': 5
        }
        response = self.client.patch(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        rating.refresh_from_db()
        self.assertEqual(rating.value, 3) # Value should remain unchanged

    def test_delete_rating_authenticated_owner(self):
        """
        Ensure an authenticated user can delete their own rating.
        """
        rating = Rating.objects.create(user=self.user1, media_content=self.media1, value=3)
        detail_url = reverse('rating-detail', kwargs={'pk': rating.rating_id})

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token1)
        response = self.client.delete(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Rating.objects.count(), 0)

    def test_delete_rating_authenticated_not_owner(self):
        """
        Ensure an authenticated user cannot delete another user's rating.
        """
        rating = Rating.objects.create(user=self.user1, media_content=self.media1, value=3)
        detail_url = reverse('rating-detail', kwargs={'pk': rating.rating_id})

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token2) # User2 tries to delete User1's rating
        response = self.client.delete(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Rating.objects.count(), 1) # Rating should still exist