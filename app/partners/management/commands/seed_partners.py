from django.core.management.base import BaseCommand

from app.partners.models import Partner

PARTNERS = [
    {
        'name': 'Tanzania National Parks Authority',
        'slug': 'tanzania-national-parks-authority',
        'description': 'TANAPA manages and develops Tanzania\'s 22 national parks, covering over 42,000 square kilometres. They are the main authority for wildlife conservation and park regulations.',
        'tier': 'platinum',
        'website': 'https://www.tanzaniaparks.go.tz',
        'email': 'info@tanzaniaparks.go.tz',
    },
    {
        'name': 'Tanzania Tourist Board',
        'slug': 'tanzania-tourist-board',
        'description': 'The Tanzania Tourist Board promotes Tanzania as a tourist destination internationally. They regulate tourism activities, license operators, and provide official tourism statistics.',
        'tier': 'platinum',
        'website': 'https://www.tanzaniatourism.go.tz',
        'email': 'info@tanzaniatourism.go.tz',
    },
    {
        'name': 'Ngorongoro Conservation Area Authority',
        'slug': 'ngorongoro-conservation-area-authority',
        'description': 'The NCAA manages the Ngorongoro Conservation Area, a unique multiple land-use area that combines wildlife conservation with the traditional lifestyle of the Maasai people.',
        'tier': 'gold',
        'website': 'https://www.ncaa.go.tz',
        'email': 'info@ncaa.go.tz',
    },
    {
        'name': 'Wildlife Conservation Society Tanzania',
        'slug': 'wildlife-conservation-society-tanzania',
        'description': 'WCS Tanzania works to protect wildlife and wild places across the country. Their programs focus on anti-poaching, community conservation, and marine protected areas.',
        'tier': 'gold',
        'website': 'https://tanzania.wcs.org',
        'email': 'tanzania@wcs.org',
    },
    {
        'name': 'African Wildlife Foundation',
        'slug': 'african-wildlife-foundation',
        'description': 'AWF has worked in Tanzania for over 50 years supporting conservation and sustainable development. They run programs in wildlife management, land use planning, and community livelihoods.',
        'tier': 'gold',
        'website': 'https://www.awf.org',
        'email': 'info@awf.org',
    },
    {
        'name': 'Arusha Declaration Museum',
        'slug': 'arusha-declaration-museum',
        'description': 'A cultural institution in Arusha that preserves the legacy of Tanzania\'s independence movement and the Arusha Declaration. Important for understanding Tanzania\'s political and cultural history.',
        'tier': 'silver',
        'website': 'https://www.arushadeclarationmuseum.go.tz',
        'email': '',
    },
    {
        'name': 'Zanzibar Commission for Tourism',
        'slug': 'zanzibar-commission-for-tourism',
        'description': 'The ZCT regulates and promotes tourism in Zanzibar. They license tourism businesses, enforce standards, and support sustainable tourism development across the archipelago.',
        'tier': 'silver',
        'website': 'https://www.zanzibartourism.go.tz',
        'email': 'info@zanzibartourism.go.tz',
    },
    {
        'name': 'Kilimanjaro Porters Assistance Project',
        'slug': 'kilimanjaro-porters-assistance-project',
        'description': 'KPAP advocates for the fair treatment of Kilimanjaro porters and promotes responsible trekking practices. They work with tour operators to improve porter welfare and wages.',
        'tier': 'community',
        'website': 'https://www.kiliporters.org',
        'email': 'info@kiliporters.org',
    },
]


class Command(BaseCommand):
    help = 'Seed partner organizations'

    def handle(self, *args, **options):
        created = 0
        skipped = 0

        for data in PARTNERS:
            partner, is_new = Partner.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'tier': data['tier'],
                    'website': data.get('website', ''),
                    'email': data.get('email', ''),
                    'is_active': True,
                }
            )
            if is_new:
                created += 1
                self.stdout.write(f'  Created: {partner.name}')
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created} partners created, {skipped} already existed.'
        ))
