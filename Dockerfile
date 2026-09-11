# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12-slim

# ---- builder: compile wheels for everything we need at runtime ----
FROM python:${PYTHON_VERSION} AS builder

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- runtime: slim image, no compilers, non-root user ----
FROM python:${PYTHON_VERSION} AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=cofig.settings

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

COPY . .
RUN chmod +x docker/entrypoint.sh \
    && mkdir -p logs staticfiles \
    && chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health/', timeout=3)" || exit 1

ENTRYPOINT ["docker/entrypoint.sh"]
