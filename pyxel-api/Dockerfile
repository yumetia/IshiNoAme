FROM python:3.13-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# dev: has the tests, runs pytest
FROM base AS dev
RUN pip install pytest ruff
COPY . .
CMD ["pytest"]

# prod: only the app, run by gunicorn
FROM base AS prod
RUN pip install gunicorn
COPY api.py database.py ./
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} api:app"]
