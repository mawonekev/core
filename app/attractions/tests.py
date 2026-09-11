
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from app.regions.models import Region

from .models import Attraction

User = get_user_model()


def make_attraction(region, user, name='Serengeti', slug='serengeti', featured=False):
    return Attraction.objects.create(
        name=name, slug=slug, region=region,
        category='national_park', description='Great wildlife reserve.',
        short_description='Wildlife reserve.', latitude='-2.3333', longitude='34.8333',
        difficulty_level='easy', access_info='By road or air.',
        best_time_to_visit='June-October', seasonal_availability='Year-round',
        estimated_duration='3-5 days', created_by=user,
        is_active=True, is_featured=featured, is_approved=True,
    )


class AttractionsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = '/api/v1/attractions/'
        self.user = User.objects.create_user(username='attruser', email='attr@example.com', password='Pass1234!')
        self.region = Region.objects.create(
            name='Arusha', slug='arusha', description='Safari hub.',
            latitude='-3.3869', longitude='36.6830',
        )
        self.attraction = make_attraction(self.region, self.user)

    def test_list_attractions_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attraction_detail_public(self):
        response = self.client.get(f'{self.list_url}serengeti/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Serengeti')

    def test_attraction_detail_not_found(self):
        response = self.client.get(f'{self.list_url}nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_featured_attractions(self):
        make_attraction(self.region, self.user, name='Ngorongoro', slug='ngorongoro', featured=True)
        response = self.client.get(f'{self.list_url}featured/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attractions_by_category(self):
        response = self.client.get(f'{self.list_url}by_category/?category=national_park')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attractions_by_category_missing_param(self):
        response = self.client.get(f'{self.list_url}by_category/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_attractions_by_region(self):
        response = self.client.get(f'{self.list_url}by_region/?region=arusha')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attractions_by_region_missing_param(self):
        response = self.client.get(f'{self.list_url}by_region/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_attractions(self):
        response = self.client.get(f'{self.list_url}?search=Serengeti')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_attraction_requires_auth(self):
        response = self.client.post(self.list_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
