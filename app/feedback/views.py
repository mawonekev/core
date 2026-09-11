import urllib.request

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.attractions.models import Attraction

from .models import Review
from .serializers import ReviewSerializer, UserFeedbackSerializer


@extend_schema(
    tags=['Feedback'],
    summary='Submit user feedback',
    description=(
        'Submit feedback, suggestions, complaints, or inquiries.\n\n'
        'Anonymous users can submit feedback by providing `name` and `email`.\n'
        'Authenticated users will have their user linked automatically.\n\n'
        '**Email Notification**: Admin will be notified via email if SMTP is configured.'
    ),
    responses={
        201: OpenApiResponse(response=UserFeedbackSerializer, description='Feedback submitted successfully'),
        400: OpenApiResponse(description='Validation error'),
    }
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def submit_feedback(request):
    serializer = UserFeedbackSerializer(data=request.data)
    if serializer.is_valid():
        if request.user.is_authenticated:
            feedback = serializer.save(user=request.user)
        else:
            feedback = serializer.save()
        try:
            if settings.CONTACT_EMAIL:
                send_mail(
                    subject=f'[Xenohuru] New {feedback.feedback_type} — {feedback.subject}',
                    message=f'From: {feedback.name} ({feedback.email})\n\nType: {feedback.get_feedback_type_display()}\n\nMessage:\n{feedback.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
        except Exception:
            pass  # Never fail the request due to email errors
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def _get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def _detect_country(request):
    """Best-effort IP geolocation — fails silently, never blocks the request."""
    ip = _get_client_ip(request)
    if not ip or ip in ('127.0.0.1', '::1', ''):
        return ''
    try:
        with urllib.request.urlopen(f'https://ipapi.co/{ip}/country_name/', timeout=2) as r:
            return r.read().decode().strip()
    except Exception:
        return ''


@extend_schema(
    tags=['Reviews'],
    summary='List or create reviews for an attraction',
    description=(
        '**GET** — List all approved reviews for an attraction (public access).\n\n'
        '**POST** — Submit a review for an attraction. **No authentication required**.\n\n'
        '**Anonymous Reviews** (no login required):\n'
        '- Provide: `reviewer_name`, `reviewer_email`, `reviewer_country`\n'
        '- Example: `{"title": "Great place!", "body": "...", "rating": 5, '
        '"reviewer_name": "John Doe", "reviewer_email": "john@example.com", '
        '"reviewer_country": "USA"}`\n\n'
        '**Authenticated Reviews** (logged in users):\n'
        '- User info automatically linked\n'
        '- One review per user per attraction\n\n'
        '**All reviews**:\n'
        '- Require admin approval before becoming public (anti-spam protection)\n'
        '- Email notification sent to admin for moderation\n'
        '- Visible in API only after approval\n\n'
        'This allows travelers, researchers, and anyone to share feedback about Tanzania attractions.'
    ),
    parameters=[
        OpenApiParameter('slug', description='Attraction slug', required=True, type=str, location='path'),
    ],
    responses={
        200: OpenApiResponse(response=ReviewSerializer(many=True), description='List of approved reviews'),
        201: OpenApiResponse(response=ReviewSerializer, description='Review created (pending approval)'),
        400: OpenApiResponse(description='Validation error - missing required fields'),
    }
)
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def attraction_reviews(request, slug):
    attraction = get_object_or_404(Attraction, slug=slug)

    if request.method == 'GET':
        # Only show approved reviews to public
        reviews = Review.objects.filter(attraction=attraction, is_approved=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # For authenticated users, link the user and check for duplicates
            if request.user.is_authenticated:
                if Review.objects.filter(attraction=attraction, user=request.user).exists():
                    return Response(
                        {'error': 'You have already reviewed this attraction'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                review = serializer.save(user=request.user, attraction=attraction)
            else:
                # Auto-detect country from IP if not provided
                country = serializer.validated_data.get('reviewer_country') or _detect_country(request)
                review = serializer.save(attraction=attraction, reviewer_country=country or '')

            # Send email notification to admin
            try:
                if settings.CONTACT_EMAIL:
                    reviewer_info = f"{request.user.username} (authenticated)" if request.user.is_authenticated else f"{review.reviewer_name} ({review.reviewer_email}) from {review.reviewer_country}"

                    send_mail(
                        subject=f'[Xenohuru] New review for {attraction.name}',
                        message=(
                            f'A new review has been submitted and is pending approval.\n\n'
                            f'Attraction: {attraction.name}\n'
                            f'Reviewer: {reviewer_info}\n'
                            f'Rating: {review.rating}/5\n\n'
                            f'Title: {review.title}\n\n'
                            f'{review.body}\n\n'
                            f'---\n'
                            f'Approve or reject in admin panel: /admin/feedback/review/{review.id}/change/'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.CONTACT_EMAIL],
                        fail_silently=True,
                    )
            except Exception:
                pass  # Never fail the request due to email errors

            return Response(
                {
                    **serializer.data,
                    'message': 'Review submitted successfully! It will be visible after admin approval.'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Reviews'],
    summary='Retrieve, update or delete a review',
    description=(
        '**GET** — View review details (approved reviews are public).\n\n'
        '**PATCH/PUT** — Update your own review or admin can update any review.\n\n'
        '**DELETE** — Delete your own review or admin can delete any review.\n\n'
        '**Permissions**:\n'
        '- Users can only edit/delete their own reviews\n'
        '- Admin/staff can moderate all reviews\n'
    ),
    responses={
        200: OpenApiResponse(response=ReviewSerializer, description='Review details'),
        204: OpenApiResponse(description='Review deleted successfully'),
        403: OpenApiResponse(description='Permission denied - not your review'),
        404: OpenApiResponse(description='Review not found or not approved'),
    }
)
@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])  # Permission checked in view logic
@csrf_exempt
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'GET':
        # Only show unapproved reviews to the author or staff
        if not review.is_approved and request.user != review.user and not request.user.is_staff:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method in ['PATCH', 'PUT']:
        # Only the author or staff can edit
        if request.user != review.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied - you can only edit your own reviews'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ReviewSerializer(review, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Only the author or staff can delete
        if request.user == review.user or request.user.is_staff:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Permission denied - you can only delete your own reviews'},
            status=status.HTTP_403_FORBIDDEN
        )
