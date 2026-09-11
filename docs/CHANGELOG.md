# Changelog

All notable changes to this project are documented here. Format loosely
follows [Keep a Changelog](https://keepachangelog.com/); versions follow
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-09-11

First public release, under the GNU General Public License v3.0.

- Relicensed from MIT to GPLv3
- Added Docker support: multi-stage `Dockerfile`, `docker-compose.yml`
  (Postgres + app), health-checked container startup
- Added Jenkins pipeline (`Jenkinsfile`): lint, build, test against the
  built image, tag releases, deploy `main` on green
- Removed GitHub Actions in favor of Jenkins as the sole CI/CD path
- Hardened settings: `SECRET_KEY` must now come from the environment,
  no insecure fallback baked into source
- Removed unused `python-dotenv` dependency and a stray backup file from
  the attractions seed command
- Cleaned up `.gitignore` and fixed broken references in the README

## [2026-03-19]

- Added soft delete and approval workflow to all content models
- Added API usage tracking middleware
- Added Statistics model (singleton) to track system totals
- Added Tag model for categorizing content
- Reusable mixins added: ContactMixin, ImageMixin, PriceMixin, PublishMixin
- Fixed SEO field lengths that were causing DataError on fixture load
- All 31 Tanzania regions added to fixtures with GPS coords and descriptions
- ReadOnlyOrAdmin permission class added (public can only read, write = admin only)
- Email verification system added (register → verify email → full access)
- Rate limiting added (100/hr anon, 1000/hr auth)
- Anonymous review submission enabled with duplicate prevention by email
- Feedback/contact form endpoint added
- Weather integration added via Open-Meteo API
- Scientific citations system added to attractions
- Endemic species tracking with conservation status

## [2026-03-15]

- Initial project structure
- Accounts app with JWT auth
- Attractions and Regions apps
- Blog app
- Operators and Partners apps
- Feedback and Reviews app
- Weather app
- Media upload app
- Itinerary app
- Contributors / creator profiles app
- Announcements app
