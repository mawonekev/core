# Contributing

Thanks for checking this out. Contributions are welcome.

---

## Ways to help

**Content** — know a good attraction in Tanzania that's not listed? Open an issue with "New Attraction:" in the title and include the location, coordinates, and a description.

**Bug fixes** — found something broken? Open an issue or submit a PR.

**Code improvements** — new features, performance, tests, whatever. Open an issue first for bigger changes so we can discuss it before you do the work.

**Documentation** — if something in the docs is confusing or wrong, fix it.

---

## Dev setup

See [DEPLOYMENT.md](../DEPLOYMENT.md) for getting the project running locally.

---

## Submitting a PR

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-thing`
3. Make your changes
4. Test it works: `python manage.py test`
5. Push and open a PR

Branch names: `feature/`, `fix/`, `docs/` prefix makes it easier to scan.

Commit messages: just be descriptive. `feat: add review flagging` is better than `update views.py`.

---

## Database changes

If your PR touches models, include the migration:

```bash
python manage.py makemigrations
```

And test that it applies cleanly on a fresh database.

---

## Code style

- Follow existing patterns in the codebase
- Don't over-engineer simple things
- Add comments where the logic isn't obvious

---

## Content moderation rules

For attraction submissions:
- Coordinates must be accurate
- Description should be factual, not promotional
- Include difficulty level if it's a physical activity

We'll reject submissions that are spam, duplicate, or clearly inaccurate.

---

Questions? Open an issue or email xenohuru@gmail.com
