FROM python:3.12

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --timeout=300 --retries=5 --no-cache-dir -r requirements.txt

COPY infra/docker/entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY --chown=appuser:appuser src/ .
RUN mkdir -p /app/sent_emails && chown appuser:appuser /app/sent_emails

USER appuser

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "blogicum.wsgi:application"]
