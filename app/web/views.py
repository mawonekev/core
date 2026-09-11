import json

from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from app.attractions.models import Attraction
from app.blog.models import Article
from app.itinerary.models import Itinerary
from app.regions.models import Region

GYG_PARTNER_ID     = getattr(settings, 'GYG_PARTNER_ID', 'J8EVQ8S')
GOOGLE_MAPS_API_KEY = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')

_ATTRACTION_Q = Q(is_approved=True, deleted_at__isnull=True, is_active=True)
_REGION_Q     = Q(is_approved=True, deleted_at__isnull=True)
_ARTICLE_Q    = Q(is_approved=True, status='published', deleted_at__isnull=True)


def home(request):
    from django.utils import timezone

    from app.announcements.models import Announcement
    from app.feedback.models import Review
    from app.partners.models import Partner

    now = timezone.now()
    announcement = (
        Announcement.objects
        .filter(is_active=True)
        .filter(Q(starts_at__isnull=True) | Q(starts_at__lte=now))
        .filter(Q(ends_at__isnull=True)   | Q(ends_at__gte=now))
        .order_by('-priority', '-id')
        .first()
    )
    return render(request, 'pages/home.html', {
        'featured_attractions': Attraction.objects.filter(_ATTRACTION_Q, is_featured=True).select_related('region')[:8],
        'regions':              Region.objects.filter(_REGION_Q)[:6],
        'latest_articles':      Article.objects.filter(_ARTICLE_Q).select_related('author').order_by('-published_at')[:3],
        'latest_reviews':       Review.objects.filter(is_approved=True).select_related('attraction').order_by('-created_at')[:14],
        'partners':             Partner.objects.filter(is_active=True).order_by('tier', 'name'),
        'announcement':         announcement,
        'stats': {
            'attractions': Attraction.objects.filter(_ATTRACTION_Q).count(),
            'regions':     Region.objects.filter(_REGION_Q).count(),
        },
        'gyg_partner_id': GYG_PARTNER_ID,
    })


def attraction_list(request):
    qs = Attraction.objects.filter(_ATTRACTION_Q).select_related('region')
    category   = request.GET.get('category', '')
    region_slug = request.GET.get('region', '')
    difficulty = request.GET.get('difficulty', '')
    q          = request.GET.get('q', '')

    if category:
        qs = qs.filter(category=category)
    if region_slug:
        qs = qs.filter(region__slug=region_slug)
    if difficulty:
        qs = qs.filter(difficulty_level=difficulty)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(short_description__icontains=q))

    return render(request, 'pages/attractions/list.html', {
        'attractions': qs,
        'regions': Region.objects.filter(_REGION_Q),
        'categories': Attraction.CATEGORY_CHOICES,
        'difficulties': Attraction.DIFFICULTY_CHOICES,
        'filters': {'category': category, 'region': region_slug, 'difficulty': difficulty, 'q': q},
        'total': qs.count(),
    })


def attraction_detail(request, slug):
    from app.operators.models import TourOperator
    attraction = get_object_or_404(
        Attraction.objects.filter(_ATTRACTION_Q)
                  .select_related('region')
                  .prefetch_related('endemic_species', 'tips', 'transport_facilities', 'citations', 'images'),
        slug=slug,
    )
    related   = Attraction.objects.filter(_ATTRACTION_Q, region=attraction.region).exclude(pk=attraction.pk)[:6]
    operators = TourOperator.objects.filter(is_approved=True, is_active=True, deleted_at__isnull=True, attractions=attraction)
    gyg_id    = attraction.gyg_location_id or attraction.region.gyg_location_id
    return render(request, 'pages/attractions/detail.html', {
        'attraction': attraction,
        'related':    related,
        'operators':  operators,
        'gyg_partner_id': GYG_PARTNER_ID,
        'gyg_location_id': gyg_id,
        'google_maps_api_key': GOOGLE_MAPS_API_KEY,
    })


def region_list(request):
    regions = Region.objects.filter(_REGION_Q)
    return render(request, 'pages/regions/list.html', {'regions': regions})


def region_detail(request, slug):
    region      = get_object_or_404(Region.objects.filter(_REGION_Q), slug=slug)
    attractions = Attraction.objects.filter(_ATTRACTION_Q, region=region).select_related('region')
    categories  = attractions.values_list('category', flat=True).distinct()
    boundary_json = json.dumps(region.boundary_geojson) if region.boundary_geojson else ''
    return render(request, 'pages/regions/detail.html', {
        'region': region,
        'attractions': attractions,
        'categories': list(categories),
        'gyg_partner_id': GYG_PARTNER_ID,
        'gyg_location_id': region.gyg_location_id,
        'google_maps_api_key': GOOGLE_MAPS_API_KEY,
        'boundary_json': boundary_json,
    })


def blog_list(request):
    articles = Article.objects.filter(_ARTICLE_Q).select_related('author').order_by('-published_at')
    return render(request, 'pages/blog/list.html', {'articles': articles})


def blog_detail(request, slug):
    article = get_object_or_404(
        Article.objects.filter(_ARTICLE_Q).select_related('author'), slug=slug,
    )
    related = Article.objects.filter(_ARTICLE_Q).exclude(pk=article.pk).order_by('-published_at')[:3]
    return render(request, 'pages/blog/detail.html', {'article': article, 'related': related})


def itineraries(request):
    items = Itinerary.objects.filter(is_public=True).prefetch_related('days', 'featured_attractions').order_by('-created_at')
    return render(request, 'pages/itineraries.html', {'itineraries': items})


def itinerary_detail(request, slug):
    item = get_object_or_404(Itinerary, slug=slug, is_public=True)
    return render(request, 'pages/itinerary_detail.html', {'itinerary': item})


def search(request):
    q = request.GET.get('q', '').strip()
    attractions = []
    articles    = []
    if q:
        attractions = Attraction.objects.filter(_ATTRACTION_Q).filter(
            Q(name__icontains=q) | Q(short_description__icontains=q)
        ).select_related('region')[:12]
        articles = Article.objects.filter(_ARTICLE_Q).filter(
            Q(title__icontains=q) | Q(excerpt__icontains=q)
        )[:6]
    return render(request, 'pages/search.html', {
        'q': q,
        'attractions': attractions,
        'articles': articles,
        'total': len(attractions) + len(articles),
    })


def weather(request):
    regions = Region.objects.filter(_REGION_Q).values('name', 'slug', 'latitude', 'longitude')
    return render(request, 'pages/weather.html', {'regions': regions})


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')


def faq(request):
    return render(request, 'pages/faq.html')


def contributors(request):
    return render(request, 'pages/contributors.html')


def sponsor(request):
    return render(request, 'pages/sponsor.html')
