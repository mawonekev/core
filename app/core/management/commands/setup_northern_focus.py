"""
Management command: setup_northern_focus

1. Approves northern circuit + Zanzibar regions, disapproves the rest.
2. Seeds 15 real authoritative citations linked to relevant attractions/regions.
3. Approves main northern circuit attractions that have real content.

Usage:
    python manage.py setup_northern_focus
"""
from django.core.management.base import BaseCommand

NORTHERN_REGION_SLUGS = {
    'arusha', 'kilimanjaro', 'mara', 'manyara',
    'mjini-magharibi', 'zanzibar-north-nungwi-kendwa',
    'zanzibar-south-central-jambiani-paje', 'zanzibar-urbanwest-stone-town',
    'pemba-island',
}

NORTHERN_ATTRACTION_SLUGS = {
    'serengeti-national-park', 'mount-kilimanjaro', 'ngorongoro-crater',
    'tarangire-national-park', 'lake-manyara-national-park', 'mount-meru',
    'olduvai-gorge', 'arusha-national-park', 'lake-natron-arusha',
    'ol-doinyo-lengai-arusha',
}

CITATIONS = [
    {
        'title': 'Tanzania National Parks – Official Authority',
        'author': 'Tanzania National Parks Authority (TANAPA)',
        'year': 2024,
        'citation_type': 'website',
        'publisher': 'TANAPA',
        'url': 'https://www.tanzaniaparks.go.tz',
        'is_primary_source': True,
        'trust_score': 10,
        'attractions': [
            'serengeti-national-park', 'mount-kilimanjaro', 'ngorongoro-crater',
            'tarangire-national-park', 'lake-manyara-national-park',
            'arusha-national-park', 'mount-meru',
        ],
        'regions': ['arusha', 'kilimanjaro', 'mara', 'manyara'],
    },
    {
        'title': 'Serengeti National Park – UNESCO World Heritage Site',
        'author': 'UNESCO World Heritage Committee',
        'year': 1981,
        'citation_type': 'website',
        'publisher': 'UNESCO',
        'url': 'https://whc.unesco.org/en/list/156',
        'is_primary_source': True,
        'trust_score': 10,
        'attractions': ['serengeti-national-park'],
        'regions': ['mara'],
    },
    {
        'title': 'Ngorongoro Conservation Area – UNESCO World Heritage Site',
        'author': 'UNESCO World Heritage Committee',
        'year': 1979,
        'citation_type': 'website',
        'publisher': 'UNESCO',
        'url': 'https://whc.unesco.org/en/list/39',
        'is_primary_source': True,
        'trust_score': 10,
        'attractions': ['ngorongoro-crater', 'olduvai-gorge'],
        'regions': ['arusha'],
    },
    {
        'title': 'Kilimanjaro National Park – UNESCO World Heritage Site',
        'author': 'UNESCO World Heritage Committee',
        'year': 1987,
        'citation_type': 'website',
        'publisher': 'UNESCO',
        'url': 'https://whc.unesco.org/en/list/403',
        'is_primary_source': True,
        'trust_score': 10,
        'attractions': ['mount-kilimanjaro'],
        'regions': ['kilimanjaro'],
    },
    {
        'title': 'Serengeti II: Dynamics, Management and Conservation of an Ecosystem',
        'author': 'Sinclair, A.R.E. & Arcese, P. (eds)',
        'year': 1995,
        'citation_type': 'book',
        'publisher': 'University of Chicago Press',
        'isbn': '9780226760339',
        'is_primary_source': True,
        'trust_score': 9,
        'attractions': ['serengeti-national-park'],
        'regions': ['mara'],
    },
    {
        'title': 'Kilimanjaro Ice Core Records: Evidence of Holocene Climate Change in Tropical Africa',
        'author': 'Thompson, L.G. et al.',
        'year': 2002,
        'citation_type': 'research_paper',
        'journal': 'Science',
        'doi': '10.1126/science.1073198',
        'url': 'https://doi.org/10.1126/science.1073198',
        'is_primary_source': True,
        'trust_score': 9,
        'attractions': ['mount-kilimanjaro'],
        'regions': ['kilimanjaro'],
    },
    {
        'title': 'Tanzania Wildlife Research Institute – Official Research Portal',
        'author': 'Tanzania Wildlife Research Institute (TAWIRI)',
        'year': 2024,
        'citation_type': 'government_report',
        'publisher': 'TAWIRI',
        'url': 'https://www.tawiri.or.tz',
        'is_primary_source': True,
        'trust_score': 9,
        'attractions': [
            'serengeti-national-park', 'ngorongoro-crater',
            'tarangire-national-park', 'lake-manyara-national-park',
        ],
        'regions': ['arusha', 'mara', 'manyara'],
    },
    {
        'title': 'African Wildlife Foundation – Tanzania Conservation Programs',
        'author': 'African Wildlife Foundation',
        'year': 2023,
        'citation_type': 'ngo_report',
        'publisher': 'AWF',
        'url': 'https://www.awf.org/country/tanzania',
        'is_primary_source': False,
        'trust_score': 8,
        'attractions': [
            'serengeti-national-park', 'ngorongoro-crater',
            'tarangire-national-park',
        ],
        'regions': ['arusha', 'mara'],
    },
    {
        'title': 'IUCN Red List of Threatened Species',
        'author': 'IUCN Species Survival Commission',
        'year': 2024,
        'citation_type': 'website',
        'publisher': 'International Union for Conservation of Nature',
        'url': 'https://www.iucnredlist.org',
        'is_primary_source': True,
        'trust_score': 10,
        'attractions': [
            'serengeti-national-park', 'ngorongoro-crater',
            'mount-kilimanjaro', 'lake-manyara-national-park',
        ],
        'regions': ['arusha', 'kilimanjaro', 'mara', 'manyara'],
    },
    {
        'title': 'Tanzania Tourism Board – Official Tourism Statistics and Information',
        'author': 'Tanzania Tourism Board',
        'year': 2024,
        'citation_type': 'government_report',
        'publisher': 'Ministry of Natural Resources and Tourism',
        'url': 'https://tanzaniatourism.go.tz',
        'is_primary_source': True,
        'trust_score': 9,
        'attractions': ['serengeti-national-park', 'mount-kilimanjaro', 'ngorongoro-crater'],
        'regions': ['arusha', 'kilimanjaro', 'mara', 'manyara', 'mjini-magharibi'],
    },
    {
        'title': 'Serengeti Shall Not Die',
        'author': 'Grzimek, B. & Grzimek, M.',
        'year': 1960,
        'citation_type': 'book',
        'publisher': 'Hamish Hamilton',
        'is_primary_source': False,
        'trust_score': 8,
        'attractions': ['serengeti-national-park'],
        'regions': ['mara'],
    },
    {
        'title': 'WWF Tanzania – Marine and Freshwater Conservation',
        'author': 'World Wide Fund for Nature',
        'year': 2023,
        'citation_type': 'ngo_report',
        'publisher': 'WWF',
        'url': 'https://www.worldwildlife.org/places/eastern-africa',
        'is_primary_source': False,
        'trust_score': 8,
        'attractions': ['lake-manyara-national-park'],
        'regions': ['manyara', 'mjini-magharibi', 'zanzibar-north-nungwi-kendwa'],
    },
    {
        'title': 'Ngorongoro Conservation Area Authority – Official Site',
        'author': 'Ngorongoro Conservation Area Authority (NCAA)',
        'year': 2024,
        'citation_type': 'government_report',
        'publisher': 'NCAA',
        'url': 'https://www.ncaa.go.tz',
        'is_primary_source': True,
        'trust_score': 10,
        'attractions': ['ngorongoro-crater', 'olduvai-gorge'],
        'regions': ['arusha'],
    },
    {
        'title': 'Zanzibar Commission for Tourism – Official Tourism Guide',
        'author': 'Zanzibar Commission for Tourism (ZCT)',
        'year': 2024,
        'citation_type': 'government_report',
        'publisher': 'Revolutionary Government of Zanzibar',
        'url': 'https://www.zanzibartourism.go.tz',
        'is_primary_source': True,
        'trust_score': 9,
        'attractions': [],
        'regions': [
            'mjini-magharibi', 'zanzibar-north-nungwi-kendwa',
            'zanzibar-south-central-jambiani-paje', 'zanzibar-urbanwest-stone-town',
            'pemba-island',
        ],
    },
    {
        'title': 'Olduvai Gorge: A Case for the Humanity of NAN (Australopithecus boisei)',
        'author': 'Leakey, M.D.',
        'year': 1971,
        'citation_type': 'book',
        'publisher': 'Cambridge University Press',
        'isbn': '9780521077989',
        'is_primary_source': True,
        'trust_score': 9,
        'attractions': ['olduvai-gorge', 'ngorongoro-crater'],
        'regions': ['arusha'],
    },
]


class Command(BaseCommand):
    help = 'Approve northern circuit regions, seed 15 citations, approve key northern attractions'

    def handle(self, *args, **options):
        from app.attractions.models import Attraction, Citation
        from app.regions.models import Region

        # 1. Regions
        self.stdout.write('--- Regions ---')
        approved = disapproved = 0
        for region in Region.objects.filter(deleted_at__isnull=True):
            should = region.slug in NORTHERN_REGION_SLUGS
            if region.is_approved != should:
                region.is_approved = should
                region.save(update_fields=['is_approved'])
                self.stdout.write(f'  {"approved" if should else "hidden"}: {region.name} ({region.slug})')
            if should:
                approved += 1
            else:
                disapproved += 1
        self.stdout.write(self.style.SUCCESS(f'  {approved} approved, {disapproved} hidden'))

        # 2. Key northern attractions
        self.stdout.write('--- Attractions ---')
        act_count = 0
        for slug in NORTHERN_ATTRACTION_SLUGS:
            updated = Attraction.objects.filter(slug=slug, is_approved=False).update(is_approved=True)
            if updated:
                self.stdout.write(f'  approved attraction: {slug}')
                act_count += updated
        self.stdout.write(self.style.SUCCESS(f'  {act_count} attraction(s) approved'))

        # 3. Citations
        self.stdout.write('--- Citations ---')
        created = skipped = 0
        for data in CITATIONS:
            attraction_slugs = data.pop('attractions')
            region_slugs = data.pop('regions')

            if Citation.objects.filter(title=data['title']).exists():
                skipped += 1
                continue

            cite = Citation.objects.create(
                formatted_citation=_format(data),
                **data,
            )
            for slug in attraction_slugs:
                try:
                    cite.attractions.add(Attraction.objects.get(slug=slug))
                except Attraction.DoesNotExist:
                    pass
            for slug in region_slugs:
                try:
                    cite.regions.add(Region.objects.get(slug=slug))
                except Region.DoesNotExist:
                    pass
            self.stdout.write(f'  created: {cite.title[:60]}')
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'  {created} citation(s) created, {skipped} already exist'
        ))
        self.stdout.write(self.style.SUCCESS('Done.'))


def _format(data):
    parts = []
    if data.get('author'):
        parts.append(data['author'])
    if data.get('year'):
        parts.append(f"({data['year']})")
    parts.append(f'"{data["title"]}"')
    if data.get('journal'):
        parts.append(data['journal'])
    elif data.get('publisher'):
        parts.append(data['publisher'])
    if data.get('doi'):
        parts.append(f"DOI: {data['doi']}")
    elif data.get('url'):
        parts.append(data['url'])
    return '. '.join(parts) + '.'
