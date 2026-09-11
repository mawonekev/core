"""
Management command: load_content_data
Reads attraction/region JSON files from xenohuru-ui-core/content/ and updates
the matching DB records with richer descriptions and GYG location IDs.

Skips: sections, faqs, gygUrl, gygLabel, gygNote  (heavy / not needed)
Updates: description (from intro), gyg_location_id, and AttractionTip records.

Usage:
    python manage.py load_content_data
    python manage.py load_content_data --content-dir /path/to/content
    python manage.py load_content_data --clear-tips  # remove existing tips first
"""

import json
import os

from django.core.management.base import BaseCommand

from app.attractions.models import Attraction, AttractionTip
from app.regions.models import Region

ATTRACTION_SLUG_ALIASES = {
    'ngorongoro-conservation-area': 'ngorongoro-crater',
    'pemba-island': 'pemba-diving',
    'stone-town-zanzibar': None,
    'zanzibar-archipelago': None,
}

CONTENT_DIR_DEFAULT = os.path.join(
    os.path.dirname(__file__),
    '..', '..', '..', '..', '..',
    'xenohuru-ui-core', 'content',
)


class Command(BaseCommand):
    help = 'Load content JSON data into Attraction and Region records'

    def add_arguments(self, parser):
        parser.add_argument('--content-dir', default=None, help='Path to content/ directory')
        parser.add_argument('--clear-tips', action='store_true', help='Remove existing tips before adding new ones')

    def handle(self, *args, **options):
        base = os.path.abspath(options['content_dir'] or CONTENT_DIR_DEFAULT)
        if not os.path.isdir(base):
            self.stderr.write(f'Content dir not found: {base}')
            return

        gyg_map = self._load_gyg_map(base)
        self._load_regions(base, gyg_map)
        self._load_attractions(base, gyg_map, clear_tips=options['clear_tips'])
        self.stdout.write(self.style.SUCCESS('Done.'))

    # ── helpers ────────────────────────────────────────────────────────────────

    def _load_gyg_map(self, base):
        path = os.path.join(base, 'gyg-locations.json')
        if not os.path.exists(path):
            return {}
        with open(path) as f:
            data = json.load(f)
        return {loc['slug']: loc['gygId'] for loc in data.get('locations', [])}

    def _load_regions(self, base, gyg_map):
        regions_dir = os.path.join(base, 'regions')
        if not os.path.isdir(regions_dir):
            return
        for fname in sorted(os.listdir(regions_dir)):
            if not fname.endswith('.json'):
                continue
            slug = fname[:-5]
            try:
                region = Region.objects.get(slug=slug)
            except Region.DoesNotExist:
                self.stdout.write(f'  region not found: {slug} — skipped')
                continue

            with open(os.path.join(regions_dir, fname)) as f:
                data = json.load(f)

            updated = []
            intro = data.get('intro', '').strip()
            if intro and not region.description:
                region.description = intro
                updated.append('description')
            elif intro and len(intro) > len(region.description or ''):
                region.description = intro
                updated.append('description')

            gyg_id = str(data.get('gygLocationId') or gyg_map.get(slug) or '').strip()
            if gyg_id and not region.gyg_location_id:
                region.gyg_location_id = gyg_id
                updated.append('gyg_location_id')

            if updated:
                region.save(update_fields=updated)
                self.stdout.write(f'  region {slug}: updated {updated}')
            else:
                self.stdout.write(f'  region {slug}: no changes')

    def _load_attractions(self, base, gyg_map, clear_tips=False):
        attractions_dir = os.path.join(base, 'attractions')
        if not os.path.isdir(attractions_dir):
            return
        for fname in sorted(os.listdir(attractions_dir)):
            if not fname.endswith('.json'):
                continue
            slug = fname[:-5]
            db_slug = ATTRACTION_SLUG_ALIASES.get(slug, slug)
            if db_slug is None:
                self.stdout.write(f'  attraction {slug}: no alias defined — skipped')
                continue
            try:
                attraction = Attraction.objects.get(slug=db_slug)
            except Attraction.DoesNotExist:
                self.stdout.write(f'  attraction not found: {db_slug} — skipped')
                continue

            with open(os.path.join(attractions_dir, fname)) as f:
                data = json.load(f)

            updated = []
            intro = data.get('intro', '').strip()
            if intro and len(intro) > len(attraction.description or ''):
                attraction.description = intro
                updated.append('description')

            gyg_id = str(data.get('gygLocationId') or gyg_map.get(slug) or '').strip()
            if gyg_id and not attraction.gyg_location_id:
                attraction.gyg_location_id = gyg_id
                updated.append('gyg_location_id')

            if updated:
                attraction.save(update_fields=updated)

            tips_added = self._apply_tips(attraction, data.get('tips', []), clear_tips)
            self.stdout.write(
                f'  attraction {slug}: updated {updated}, tips +{tips_added}'
            )

    def _apply_tips(self, attraction, tips, clear_first):
        if not tips:
            return 0
        if clear_first:
            AttractionTip.objects.filter(attraction=attraction).delete()
        existing_titles = set(
            AttractionTip.objects.filter(attraction=attraction).values_list('title', flat=True)
        )
        count = 0
        for tip_text in tips:
            tip_text = tip_text.strip()
            if not tip_text:
                continue
            title = tip_text[:100].rsplit(' ', 1)[0] if len(tip_text) > 100 else tip_text
            if title in existing_titles:
                continue
            AttractionTip.objects.create(
                attraction=attraction,
                title=title,
                description=tip_text,
            )
            existing_titles.add(title)
            count += 1
        return count
