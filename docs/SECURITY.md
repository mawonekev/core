# Security

## Permission model

Public users can read everything (GET requests). Creating or editing content requires admin/staff access.

This is intentional — we want to prevent fake tour operators, scam listings and false information from being submitted without review.

| Action | Anonymous | Authenticated | Admin/Staff |
|--------|-----------|---------------|-------------|
| Read (GET) | yes | yes | yes |
| Submit review/feedback | yes | yes | yes |
| Create attractions, operators, etc. | no | no | yes |
| Edit content | no | no | yes |

The only public write endpoints are:
- `POST /api/v1/auth/register/` — account registration
- `POST /api/v1/feedback/submit/` — contact/feedback form
- `POST /api/v1/feedback/attractions/<slug>/reviews/` — submit a review

---

## Reporting a vulnerability

Don't open a public issue for security problems. Email xenohuru@gmail.com directly and we'll handle it privately.

---

## Getting a business listed

If you're a tour operator or partner and want to be listed:

Email xenohuru@gmail.com with your business details (registration docs, website, contacts). We'll verify and create the listing.

---

## API abuse

All API requests are logged. Rate limits are in place (100/hr anonymous, 1000/hr authenticated). Excessive scraping or attack patterns will get blocked.
