from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Region

User = get_user_model()


class RegionsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = '/api/v1/regions/'
        self.user = User.objects.create_user(username='regionuser', email='region@example.com', password='Pass1234!', is_staff=True)
        self.region = Region.objects.create(
            name='Kilimanjaro',
            slug='kilimanjaro',
            description='Home of Africa\'s highest peak.',
            latitude='-3.0674',
            longitude='37.3556',
            is_approved=True,
        )

    def test_list_regions_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_region_detail_public(self):
        response = self.client.get(f'{self.list_url}kilimanjaro/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Kilimanjaro')

    def test_region_detail_not_found(self):
        response = self.client.get(f'{self.list_url}nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_region_requires_auth(self):
        data = {'name': 'Zanzibar', 'slug': 'zanzibar', 'description': 'Island paradise.',
                'latitude': '-6.1522', 'longitude': '39.1922'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_region_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Zanzibar', 'slug': 'zanzibar', 'description': 'Island paradise.',
                'latitude': '-6.1522', 'longitude': '39.1922'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_region_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{self.list_url}kilimanjaro/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
