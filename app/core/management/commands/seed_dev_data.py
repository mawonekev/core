"""
Management command: seed_dev_data
Creates representative sample records for every model that is empty,
so all admin sections and frontend pages render properly during development.

Usage:
    python manage.py seed_dev_data
    python manage.py seed_dev_data --clear   # wipe and re-seed
"""

import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed development sample data for all empty models.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear seeded data before re-seeding.')

    def handle(self, *args, **options):
        if options['clear']:
            self._clear()

        staff = User.objects.filter(is_staff=True).first()
        self._seed_announcements()
        self._seed_creators(staff)
        self._seed_seasonal_patterns()
        self._seed_reviews()
        self._seed_attraction_inlines(staff)
        self.stdout.write(self.style.SUCCESS('Sample data seeded successfully.'))

    # ------------------------------------------------------------------
    def _clear(self):
        from app.announcements.models import Announcement
        from app.attractions.models import AttractionBoundary, AttractionTip, EndemicSpecies, NearestTransport
        from app.contributors.models import CreatorProfile
        from app.feedback.models import Review
        from app.weather.models import SeasonalWeatherPattern

        Announcement.objects.filter(title__startswith='[Dev]').delete()
        CreatorProfile.objects.filter(username__startswith='dev_').delete()
        SeasonalWeatherPattern.objects.all().delete()
        Review.objects.filter(reviewer_name__startswith='[Dev]').delete()
        # Clear inline data for the 3 seed attractions
        slugs = ['serengeti-national-park-arusha', 'ngorongoro-crater-arusha', 'mount-kilimanjaro-uhuru-peak']
        from app.attractions.models import Attraction
        for slug in slugs:
            a = Attraction.objects.filter(slug=slug).first()
            if a:
                AttractionTip.objects.filter(attraction=a).delete()
                NearestTransport.objects.filter(attraction=a).delete()
                EndemicSpecies.objects.filter(attraction=a).delete()
                AttractionBoundary.objects.filter(attraction=a).delete()
        self.stdout.write('Cleared previous seed data.')

    # ------------------------------------------------------------------
    def _seed_announcements(self):
        from app.announcements.models import Announcement

        if Announcement.objects.exists():
            self.stdout.write('  Announcements: already have data, skipping.')
            return

        records = [
            {
                'title': '[Dev] New Itineraries Launched',
                'message': 'We have just published 5 curated Tanzania itineraries — from the 7-Day Classic Safari to the 14-day Complete Tanzania adventure. Check them out under the Itineraries section.',
                'announcement_type': 'info',
                'priority': 'normal',
                'is_active': True,
                'target_url': '/itineraries/',
                'target_label': 'View Itineraries',
            },
            {
                'title': '[Dev] Planned Maintenance — 25 Apr 2025',
                'message': 'Xenohuru will be offline for approximately 30 minutes on 25 April 2025 from 02:00–02:30 EAT for scheduled database maintenance. No data will be lost.',
                'announcement_type': 'maintenance',
                'priority': 'high',
                'is_active': True,
                'starts_at': timezone.now(),
                'ends_at': timezone.now() + datetime.timedelta(days=3),
            },
            {
                'title': '[Dev] API v1 Now Public',
                'message': 'Our public REST API is now live. Developers can access all Tanzania attraction, region, and weather data — completely free. View the documentation at /api/docs/.',
                'announcement_type': 'success',
                'priority': 'normal',
                'is_active': True,
                'target_url': '/api/docs/',
                'target_label': 'API Docs',
            },
        ]

        for data in records:
            Announcement.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(f'  Announcements: created {len(records)} records.'))

    # ------------------------------------------------------------------
    def _seed_creators(self, staff):
        from app.contributors.models import CreatorProfile

        if CreatorProfile.objects.exists():
            self.stdout.write('  Creators: already have data, skipping.')
            return

        profiles = [
            {
                'username': 'dev_amara_mwangi',
                'display_name': 'Amara Mwangi',
                'bio': 'Wildlife photographer and conservation advocate based in Arusha. Has documented over 200 species across Tanzania\'s national parks. Contributor since 2024.',
                'job_title': 'Wildlife Photographer',
                'organisation': 'Serengeti Conservation Initiative',
                'expertise': 'wildlife',
                'location_city': 'Arusha',
                'location_country': 'Tanzania',
                'github_username': 'amara-mwangi',
                'twitter_handle': 'amara_tz',
                'is_public': True,
                'is_verified_creator': True,
                'joined_at': datetime.date(2024, 3, 15),
                'attractions_created': 12,
                'articles_written': 4,
                'media_uploaded': 67,
            },
            {
                'username': 'dev_jonas_weber',
                'display_name': 'Jonas Weber',
                'bio': 'Software engineer and travel blogger from Germany, living in Dar es Salaam. Contributed the initial API structure and maintains the developer documentation.',
                'job_title': 'Senior Software Engineer',
                'organisation': 'Xenohuru Core Team',
                'expertise': 'technology',
                'location_city': 'Dar es Salaam',
                'location_country': 'Tanzania',
                'github_username': 'jonas-weber-tz',
                'is_public': True,
                'is_verified_creator': True,
                'joined_at': datetime.date(2024, 1, 10),
                'attractions_created': 3,
                'articles_written': 2,
                'media_uploaded': 8,
            },
            {
                'username': 'dev_fatuma_omar',
                'display_name': 'Fatuma Omar',
                'bio': 'Local guide and cultural heritage enthusiast from Zanzibar. Specialises in Swahili Coast history, Stone Town architecture, and traditional fishing communities.',
                'job_title': 'Licensed Tour Guide',
                'organisation': 'Zanzibar Heritage Tours',
                'expertise': 'culture',
                'location_city': 'Stone Town',
                'location_country': 'Tanzania',
                'instagram_handle': 'fatuma.zanzibar',
                'is_public': True,
                'is_verified_creator': False,
                'joined_at': datetime.date(2024, 6, 20),
                'attractions_created': 8,
                'articles_written': 1,
                'media_uploaded': 24,
            },
        ]

        # Create dummy users for creators
        for i, p in enumerate(profiles, start=10):
            user, _ = User.objects.get_or_create(
                username=p['username'],
                defaults={
                    'email': f"{p['username']}@dev.xenohuru.com",
                    'first_name': p['display_name'].split()[0],
                    'last_name': p['display_name'].split()[-1],
                    'is_active': True,
                }
            )
            CreatorProfile.objects.get_or_create(
                user=user,
                defaults={k: v for k, v in p.items()},
            )

        self.stdout.write(self.style.SUCCESS(f'  Creators: created {len(profiles)} records.'))

    # ------------------------------------------------------------------
    def _seed_seasonal_patterns(self):
        from app.attractions.models import Attraction
        from app.weather.models import SeasonalWeatherPattern

        if SeasonalWeatherPattern.objects.exists():
            self.stdout.write('  Seasonal patterns: already have data, skipping.')
            return

        attraction = Attraction.objects.filter(
            deleted_at__isnull=True, is_approved=True
        ).first()

        if not attraction:
            self.stdout.write(self.style.WARNING('  Seasonal patterns: no approved attractions found, skipping.'))
            return

        patterns = [
            {
                'season_type': 'dry',
                'start_month': 6,
                'end_month': 10,
                'avg_temperature': 22.5,
                'avg_rainfall': 18.0,
                'description': (
                    'The dry season runs from June to October and is the best time to visit. '
                    'Skies are clear, wildlife concentrates around water sources making game viewing excellent, '
                    'and trails are accessible. Temperatures are warm by day (20–28°C) and cool at night (10–15°C).'
                ),
            },
            {
                'season_type': 'short_rain',
                'start_month': 11,
                'end_month': 12,
                'avg_temperature': 26.0,
                'avg_rainfall': 85.0,
                'description': (
                    'The short rains (Vuli) fall in November and December. Showers are typically brief afternoon '
                    'downpours, leaving mornings clear. The landscape turns lush green. Fewer tourists mean lower '
                    'prices and less crowded parks, though some dirt roads may become difficult.'
                ),
            },
            {
                'season_type': 'long_rain',
                'start_month': 3,
                'end_month': 5,
                'avg_temperature': 27.5,
                'avg_rainfall': 180.0,
                'description': (
                    'The long rains (Masika) from March to May bring the heaviest rainfall of the year. '
                    'Some remote parks and lodges close. The Serengeti sees the Great Migration calving season. '
                    'Not ideal for off-road driving, but birdwatching is exceptional due to migratory species.'
                ),
            },
        ]

        for p in patterns:
            SeasonalWeatherPattern.objects.create(attraction=attraction, **p)

        self.stdout.write(self.style.SUCCESS(
            f'  Seasonal patterns: created {len(patterns)} records for "{attraction.name}".'
        ))

    # ------------------------------------------------------------------
    def _seed_reviews(self):
        from app.attractions.models import Attraction
        from app.feedback.models import Review

        if Review.objects.exists():
            self.stdout.write('  Reviews: already have data, skipping.')
            return

        attraction = Attraction.objects.filter(
            deleted_at__isnull=True, is_approved=True
        ).first()

        if not attraction:
            self.stdout.write(self.style.WARNING('  Reviews: no approved attractions found, skipping.'))
            return

        reviews = [
            {
                'reviewer_name': '[Dev] Maria Kessler',
                'reviewer_country': 'Germany',
                'rating': 5,
                'body': (
                    'Absolutely breathtaking. I visited during the dry season and the visibility was perfect. '
                    'The guides were incredibly knowledgeable about the local wildlife and ecology. '
                    'This was the highlight of my entire Tanzania trip — I cannot recommend it highly enough.'
                ),
                'visit_type': 'couple',
                'visit_season': 'dry',
                'is_approved': True,
                'rating_scenery': 5,
                'rating_safety': 5,
                'rating_value_for_money': 4,
            },
            {
                'reviewer_name': '[Dev] David Okonkwo',
                'reviewer_country': 'Nigeria',
                'rating': 4,
                'body': (
                    'A must-see destination in East Africa. The early morning light is magical for photography. '
                    'Be prepared — the altitude and terrain require a reasonable level of fitness. '
                    'Carry more water than you think you need. Overall an outstanding experience.'
                ),
                'visit_type': 'solo',
                'visit_season': 'dry',
                'is_approved': True,
                'rating_scenery': 5,
                'rating_accessibility': 3,
                'rating_facilities': 4,
            },
            {
                'reviewer_name': '[Dev] Priya Sharma',
                'reviewer_country': 'India',
                'rating': 5,
                'body': (
                    'We came as a family with two teenagers and it was perfect. The rangers made everyone '
                    'feel safe and engaged. Saw lions, elephants, and a leopard all in one day. '
                    'The accommodation near the park was comfortable and staff were welcoming.'
                ),
                'visit_type': 'family',
                'visit_season': 'dry',
                'is_approved': True,
                'rating_scenery': 5,
                'rating_safety': 5,
                'rating_value_for_money': 4,
                'rating_facilities': 4,
            },
        ]

        for r in reviews:
            Review.objects.create(attraction=attraction, **r)

        self.stdout.write(self.style.SUCCESS(
            f'  Reviews: created {len(reviews)} approved records for "{attraction.name}".'
        ))

    # ------------------------------------------------------------------
    def _seed_attraction_inlines(self, staff):
        from app.attractions.models import (
            Attraction,
            AttractionBoundary,
            AttractionTip,
            EndemicSpecies,
            NearestTransport,
        )

        DATA = {
            'serengeti-national-park-arusha': {
                'tips': [
                    {
                        'title': 'Best time for the Great Migration',
                        'description': 'The river crossings at the Mara River happen July–October near Kogatende. Calving season (Jan–Feb) in the southern Serengeti offers equally dramatic viewing with predators following the herds.',
                        'created_by': staff,
                    },
                    {
                        'title': 'Book a fly-in safari for vast distances',
                        'description': 'The Serengeti is 14,763 km² — driving between zones takes 4+ hours on corrugated tracks. Internal charter flights (Coastal Aviation, Air Excel) connect Seronera, Kogatende, Grumeti, and Ndutu airstrips efficiently.',
                        'created_by': staff,
                    },
                    {
                        'title': 'Pack layers — nights are cold',
                        'description': 'Despite being near the equator, the altitude (1,500m+) makes nights cold (8–12°C). Bring a warm fleece and windproof jacket even in dry season. Mornings on game drives before 7am can be very cold.',
                        'created_by': staff,
                    },
                ],
                'transport': [
                    {
                        'transport_type': 'airport',
                        'name': 'Kilimanjaro International Airport (JRO)',
                        'distance_km': 325,
                        'travel_time_minutes': 360,
                        'is_recommended': False,
                        'description': 'Main international gateway. 6–7 hour drive via Arusha and Ngorongoro, or connect to Seronera by charter flight.',
                    },
                    {
                        'transport_type': 'airport',
                        'name': 'Seronera Airstrip (SEU)',
                        'distance_km': 0,
                        'travel_time_minutes': 0,
                        'is_recommended': True,
                        'description': 'Central Serengeti airstrip — the best way to arrive. Charter flights from Arusha ~1.5 hrs. Coastal Aviation and Air Excel operate daily scheduled services.',
                    },
                    {
                        'transport_type': 'major_city',
                        'name': 'Arusha Town',
                        'distance_km': 335,
                        'travel_time_minutes': 420,
                        'is_recommended': False,
                        'description': 'Main staging point for northern Tanzania safaris. Self-drive or guided overland via Ngorongoro Conservation Area. Road quality is rough in the wet season.',
                    },
                ],
                'species': [
                    {
                        'common_name': 'Wildebeest',
                        'scientific_name': 'Connochaetes taurinus',
                        'conservation_status': 'LC',
                        'description': 'Over 1.5 million blue wildebeest undertake the annual Great Migration — the largest overland animal movement on Earth. They follow rainfall and fresh grass in a circular route between Serengeti and Masai Mara.',
                    },
                    {
                        'common_name': 'African Lion',
                        'scientific_name': 'Panthera leo',
                        'conservation_status': 'VU',
                        'description': 'The Serengeti hosts Africa\'s largest lion population (~3,000 individuals). Large prides dominate the open plains and kopjes. Tree-climbing lions are occasionally seen resting in acacia branches.',
                    },
                    {
                        'common_name': 'Cheetah',
                        'scientific_name': 'Acinonyx jubatus',
                        'conservation_status': 'VU',
                        'description': 'The open plains of the Serengeti provide ideal hunting ground for cheetahs. Best viewed at dawn. Females often raise cubs on the Ndutu plains in the south during the dry season.',
                    },
                ],
                'boundary': {
                    'boundary_type': 'polygon',
                    'center_latitude': -2.3333,
                    'center_longitude': 34.8333,
                    'bbox_north': -1.4700,
                    'bbox_south': -3.3400,
                    'bbox_east': 35.8800,
                    'bbox_west': 33.9000,
                    'area_sq_km': 14763,
                    'elevation_min_m': 920,
                    'elevation_max_m': 1850,
                    'main_gate_name': 'Naabi Hill Gate',
                    'main_gate_latitude': -2.6350,
                    'main_gate_longitude': 34.8750,
                },
            },
            'ngorongoro-crater-arusha': {
                'tips': [
                    {
                        'title': 'Enter the crater floor before 8am',
                        'description': 'The descent road opens at 6am and the crater floor is at its best in early morning light. Animals are most active, temperatures are cool, and you will beat the midday vehicle congestion. All vehicles must exit by 6pm.',
                        'created_by': staff,
                    },
                    {
                        'title': 'Black rhino sightings require patience',
                        'description': 'The crater hosts one of Tanzania\'s last wild black rhino populations (~25 individuals). They are most often seen at Lerai Forest and Ngoitokitok Springs. Ask your driver-guide to tune into the rhino sighting radio network.',
                        'created_by': staff,
                    },
                    {
                        'title': 'Conservation fee is per vehicle per day',
                        'description': 'The crater charges USD 295 per vehicle per day in addition to the per-person conservation fee. Only 4WD vehicles are permitted on the crater floor. Visitor numbers are capped at 60 vehicles simultaneously.',
                        'created_by': staff,
                    },
                ],
                'transport': [
                    {
                        'transport_type': 'airport',
                        'name': 'Kilimanjaro International Airport (JRO)',
                        'distance_km': 200,
                        'travel_time_minutes': 210,
                        'is_recommended': True,
                        'description': 'The main gateway. 3–3.5 hour drive via Arusha on the A104 highway, then the Karatu–Lodoare Gate road. Paved all the way to the crater rim.',
                    },
                    {
                        'transport_type': 'major_city',
                        'name': 'Arusha',
                        'distance_km': 180,
                        'travel_time_minutes': 180,
                        'is_recommended': False,
                        'description': 'The standard safari base. Most operators depart Arusha at 6–7am to reach the crater floor by 9–10am. Day trips are possible but overnight stays on the rim are recommended.',
                    },
                    {
                        'transport_type': 'airport',
                        'name': 'Manyara Airstrip',
                        'distance_km': 95,
                        'travel_time_minutes': 90,
                        'is_recommended': False,
                        'description': 'Closer charter option. Coastal Aviation operates scheduled flights from Arusha. A 1.5-hour drive from Manyara through Karatu town and the NCA gate.',
                    },
                ],
                'species': [
                    {
                        'common_name': 'Black Rhinoceros',
                        'scientific_name': 'Diceros bicornis',
                        'conservation_status': 'CR',
                        'description': 'Ngorongoro Crater is one of the last strongholds for wild black rhino in Tanzania. The crater\'s enclosed ecosystem has allowed this critically endangered species to recover from near extinction in the region.',
                    },
                    {
                        'common_name': 'Flamingo',
                        'scientific_name': 'Phoeniconaias minor',
                        'conservation_status': 'NT',
                        'description': 'The soda springs at Lake Magadi on the crater floor attract thousands of lesser flamingos. The pink flocks are most visible in the dry season when the lake level is lower and the alkaline concentration higher.',
                    },
                    {
                        'common_name': 'African Elephant',
                        'scientific_name': 'Loxodonta africana',
                        'conservation_status': 'VU',
                        'description': 'The crater floor hosts a resident elephant population of mostly old bulls with large tusks. These are among the most photographed elephants in Africa. Young bulls and family herds migrate in and out of the crater seasonally.',
                    },
                ],
                'boundary': {
                    'boundary_type': 'polygon',
                    'center_latitude': -3.1700,
                    'center_longitude': 35.5900,
                    'bbox_north': -2.8800,
                    'bbox_south': -3.4100,
                    'bbox_east': 35.9200,
                    'bbox_west': 35.2600,
                    'area_sq_km': 8292,
                    'elevation_min_m': 1402,
                    'elevation_max_m': 3587,
                    'main_gate_name': 'Lodoare Gate',
                    'main_gate_latitude': -3.2850,
                    'main_gate_longitude': 35.5150,
                },
            },
            'mount-kilimanjaro-uhuru-peak': {
                'tips': [
                    {
                        'title': 'Acclimatise properly — altitude kills more climbs than fitness',
                        'description': 'Acute Mountain Sickness (AMS) is the primary reason climbers turn back. The "climb high, sleep low" principle is built into multi-day routes like Machame and Lemosho. Never rush ascent days. Diamox (acetazolamide) can help — consult your doctor before departure.',
                        'created_by': staff,
                    },
                    {
                        'title': 'Lemosho Route offers the best success rate',
                        'description': 'The 8-day Lemosho Route has a ~90% summit success rate vs ~85% for Machame and ~50% for the shorter 5-day Marangu. The extra days above 4,000m dramatically improve acclimatisation. Always choose at least 7 days.',
                        'created_by': staff,
                    },
                    {
                        'title': 'Summit night starts at midnight',
                        'description': 'All routes start the final push to Uhuru Peak around midnight to arrive at sunrise (~6–7am). Temperatures drop to -15°C to -20°C. Pack hand warmers, a balaclava, and double-layer gloves. Headtorch with fresh batteries is essential.',
                        'created_by': staff,
                    },
                ],
                'transport': [
                    {
                        'transport_type': 'airport',
                        'name': 'Kilimanjaro International Airport (JRO)',
                        'distance_km': 48,
                        'travel_time_minutes': 50,
                        'is_recommended': True,
                        'description': 'Closest international airport. Direct 50-minute drive to Moshi town via the A23 highway. Most tour operators pick up climbers directly from JRO.',
                    },
                    {
                        'transport_type': 'major_city',
                        'name': 'Moshi Town',
                        'distance_km': 27,
                        'travel_time_minutes': 40,
                        'is_recommended': False,
                        'description': 'The primary base for Kilimanjaro climbs. All KINAPA-registered operators are based here. Most climbers spend 1–2 nights acclimatising and preparing gear before the climb.',
                    },
                    {
                        'transport_type': 'bus_terminal',
                        'name': 'Arusha Bus Terminal',
                        'distance_km': 85,
                        'travel_time_minutes': 90,
                        'is_recommended': False,
                        'description': 'Regular buses and shared taxis (daladala) connect Arusha to Moshi. Journey takes 1.5–2 hours. Budget option for independent travellers not yet booked with an operator.',
                    },
                ],
                'species': [
                    {
                        'common_name': 'Kilimanjaro Tree Hyrax',
                        'scientific_name': 'Dendrohyrax validus',
                        'conservation_status': 'VU',
                        'description': 'Endemic to the Kilimanjaro forest zone (1,800–3,000m). Resembles a large guinea pig but is most closely related to elephants. Its haunting nocturnal scream echoes through the forest at night on the Machame and Lemosho routes.',
                    },
                    {
                        'common_name': 'Abbott\'s Starling',
                        'scientific_name': 'Poeoptera femoralis',
                        'conservation_status': 'VU',
                        'description': 'Rare starling found only in the montane forest of Kilimanjaro and a few other East African highlands. Glossy black with a white belly patch. Most easily spotted in the Marangu forest zone between 1,800–2,400m.',
                    },
                    {
                        'common_name': 'Kilimanjaro White-necked Raven',
                        'scientific_name': 'Corvus albicollis',
                        'conservation_status': 'LC',
                        'description': 'Iconic scavenger of the mountain that follows climbing groups to altitude camps hoping for food scraps. Highly intelligent — can open unattended bags. Frequently seen above 4,000m and on the summit plateau.',
                    },
                ],
                'boundary': {
                    'boundary_type': 'polygon',
                    'center_latitude': -3.0674,
                    'center_longitude': 37.3556,
                    'bbox_north': -2.8300,
                    'bbox_south': -3.3100,
                    'bbox_east': 37.7200,
                    'bbox_west': 37.0000,
                    'area_sq_km': 1688,
                    'elevation_min_m': 1641,
                    'elevation_max_m': 5895,
                    'main_gate_name': 'Machame Gate',
                    'main_gate_latitude': -3.1811,
                    'main_gate_longitude': 37.1278,
                },
            },
        }

        total_tips = total_transport = total_species = total_boundary = 0

        for slug, data in DATA.items():
            attraction = Attraction.objects.filter(slug=slug).first()
            if not attraction:
                self.stdout.write(self.style.WARNING(f'  Inlines: attraction "{slug}" not found, skipping.'))
                continue

            # Tips
            if not AttractionTip.objects.filter(attraction=attraction).exists():
                for t in data['tips']:
                    AttractionTip.objects.create(attraction=attraction, **t)
                total_tips += len(data['tips'])

            # Transport
            if not NearestTransport.objects.filter(attraction=attraction).exists():
                for t in data['transport']:
                    NearestTransport.objects.create(attraction=attraction, **t)
                total_transport += len(data['transport'])

            # Endemic species
            if not EndemicSpecies.objects.filter(attraction=attraction).exists():
                for s in data['species']:
                    EndemicSpecies.objects.create(attraction=attraction, **s)
                total_species += len(data['species'])

            # Boundary
            if not AttractionBoundary.objects.filter(attraction=attraction).exists():
                AttractionBoundary.objects.create(attraction=attraction, **data['boundary'])
                total_boundary += 1

        self.stdout.write(self.style.SUCCESS(
            f'  Attraction inlines: {total_tips} tips, {total_transport} transport, '
            f'{total_species} species, {total_boundary} boundaries across 3 attractions.'
        ))
