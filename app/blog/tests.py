from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from app.core.models import Tag

from .models import Article

User = get_user_model()


def make_article(author, title='Best Time to Visit Serengeti', slug='best-time-serengeti'):
    from django.utils import timezone
    return Article.objects.create(
        title=title, slug=slug,
        excerpt='Everything you need to know about timing your Serengeti visit.',
        content='# Best Time to Visit\n\nThe dry season from June to October offers...',
        author=author,
        is_published=True, published_at=timezone.now(),
        is_approved=True, status='published',
    )


class BlogAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = '/api/v1/blog/'
        self.user = User.objects.create_user(username='bloguser', email='blog@example.com', password='Pass1234!', is_staff=True)
        self.article = make_article(self.user)

    def test_list_articles_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_detail_public(self):
        response = self.client.get(f'{self.list_url}best-time-serengeti/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Best Time to Visit Serengeti')

    def test_article_detail_not_found(self):
        response = self.client.get(f'{self.list_url}nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_articles(self):
        response = self.client.get(f'{self.list_url}?search=Serengeti')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        articles = response.data.get('results', response.data)
        self.assertGreaterEqual(len(articles), 1)

    def test_filter_by_tags(self):
        tag = Tag.objects.create(name='safari', slug='safari')
        self.article.tags.add(tag)
        response = self.client.get(f'{self.list_url}?tags=safari')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        articles = response.data.get('results', response.data)
        self.assertGreaterEqual(len(articles), 1)

    def test_unpublished_article_not_listed(self):
        Article.objects.create(
            title='Draft Article', slug='draft-article',
            excerpt='This is a draft.', content='Draft content.',
            author=self.user, is_published=False,
        )
        response = self.client.get(self.list_url)
        articles = response.data.get('results', response.data)
        slugs = [a['slug'] for a in articles]
        self.assertNotIn('draft-article', slugs)

    def test_create_article_requires_auth(self):
        response = self.client.post(self.list_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_article_authenticated(self):
        self.client.force_authenticate(user=self.user)
        from django.utils import timezone
        data = {
            'title': 'Top 10 Tanzania Wildlife', 'slug': 'top-10-tanzania-wildlife',
            'excerpt': 'A guide to the top wildlife of Tanzania.',
            'content': 'Tanzania is home to...',
            'is_published': True, 'published_at': timezone.now().isoformat(),
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_article_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{self.list_url}best-time-serengeti/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
