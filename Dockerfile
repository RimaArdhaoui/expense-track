FROM python:3.12-slim

WORKDIR /app

COPY dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl gunicorn && rm -rf /tmp/*.whl

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENV DATABASE=/data/expenses.db
RUN mkdir -p /data

EXPOSE 5000
ENTRYPOINT ["docker-entrypoint.sh"]