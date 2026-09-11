from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from app.core.permissions import ReadOnlyOrAdmin

from .models import Article
from .serializers import (
    ArticleCreateUpdateSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
)

BASE_QUERYSET = Article.objects.filter(is_published=True, deleted_at__isnull=True, is_approved=True).select_related('author').prefetch_related('related_attractions')


def paginate_queryset(queryset, request, serializer_class):
    """Helper function to paginate querysets in function-based views"""
    paginator = PageNumberPagination()
    paginator.page_size = 20
    page = paginator.paginate_queryset(queryset, request)
    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=['Blog'],
    summary='List or create blog articles',
    description=(
        '**GET** — Returns all published articles ordered by publish date (newest first).\n\n'
        '| Parameter | Type | Description |\n'
        '|-----------|------|-------------|\n'
        '| `search` | string | Filter by title, excerpt, or content |\n'
        '| `tags` | string | Filter articles whose tags field contains this substring |\n\n'
        '**POST** — Create a new article. **Requires staff/admin privileges** (prevents spam/scam content). '
        'Set `is_published=true` and `published_at` to make it visible publicly.\n\n'
        '**curl GET example:**\n'
        '```bash\n'
        'curl "https://xenohuru.cleven.is-a.dev/api/v1/blog/"\n'
        '```'
    ),
    parameters=[
        OpenApiParameter('search', description='Filter by title, excerpt, or content', required=False, type=str),
        OpenApiParameter('tags', description='Filter by tag substring (e.g. `safari`)', required=False, type=str),
    ],
    request=ArticleCreateUpdateSerializer,
    responses={
        200: OpenApiResponse(response=ArticleListSerializer(many=True), description='List of published articles.'),
        201: OpenApiResponse(response=ArticleCreateUpdateSerializer, description='Article created.'),
        400: OpenApiResponse(description='Validation error.'),
        401: OpenApiResponse(description='Authentication required for POST.'),
        403: OpenApiResponse(description='Only admin/staff can create articles (anti-spam protection).'),
    },
)
@api_view(['GET', 'POST'])
@permission_classes([ReadOnlyOrAdmin])
def article_list_create(request):
    if request.method == 'GET':
        articles = BASE_QUERYSET
        search = request.query_params.get('search')
        if search:
            articles = articles.filter(title__icontains=search) | \
                       articles.filter(excerpt__icontains=search) | \
                       articles.filter(content__icontains=search)
        tags = request.query_params.get('tags')
        if tags:
            articles = articles.filter(tags__name__icontains=tags)

        # Use pagination helper
        return paginate_queryset(articles, request, ArticleListSerializer)

    serializer = ArticleCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Blog'],
    summary='Retrieve, update or delete an article',
    description=(
        'Look up an article by its `slug`.\n\n'
        '- **GET** — Public (only published articles). Returns full article including content and related attractions.\n'
        '- **PUT/PATCH** — Update. **Admin/staff only** (prevents unauthorized edits).\n'
        '- **DELETE** — Remove article. **Admin/staff only**.\n\n'
        '**curl GET example:**\n'
        '```bash\n'
        'curl https://xenohuru.cleven.is-a.dev/api/v1/blog/best-time-to-visit-serengeti/\n'
        '```'
    ),
    responses={
        200: OpenApiResponse(response=ArticleDetailSerializer, description='Full article detail.'),
        204: OpenApiResponse(description='Article deleted.'),
        401: OpenApiResponse(description='Authentication required for write operations.'),
        403: OpenApiResponse(description='Only admin/staff can modify articles.'),
        404: OpenApiResponse(description='Article not found or not published.'),
    },
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([ReadOnlyOrAdmin])
def article_detail(request, slug):
    try:
        article = BASE_QUERYSET.get(slug=slug)
    except Article.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = ArticleCreateUpdateSerializer(article, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
