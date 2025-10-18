FROM python:3.12

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --timeout=300 --retries=5 --no-cache-dir -r requirements.txt

COPY infra/docker/entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY --chown=appuser:appuser src/ .

RUN mkdir -p /app/sent_emails && chown appuser:appuser /app/sent_emails
RUN mkdir -p /app/db && chown appuser:appuser /app/db

USER appuser

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "blogicum.wsgi:application"]
