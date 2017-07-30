# Build front-end
FROM node:6.5 AS assets

WORKDIR /app

ADD src/package.json .
RUN npm install

# Configure gulp to build static assets to this dir
ENV CFG_STATIC_ROOT /app/static_compiled

ADD src/ .
RUN npm run build


# Build back-end
FROM python:3.6-slim

RUN apt-get update && apt-get install -y \
    postgresql-client libpq-dev \
    gcc gettext \
    libjpeg62-turbo-dev \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD src/requirements/requirements.txt ./requirements/requirements.txt
RUN pip install -r requirements/requirements.txt


ADD src/ .

# Copy static assets from the previous stage
COPY --from=assets /app/static_compiled /app/static_compiled

# We need to include compiled messages and static fields into a Docker image.
# SECRET_KEY is actually not so important for compilemessages and collectstatic,
# but Django now requires this to run these commands.
RUN CFG_SECRET_KEY=fake python manage.py compilemessages -v 3
RUN CFG_SECRET_KEY=fake python manage.py collectstatic --noinput

CMD uwsgi --module=wsgi \
          --processes=10 \
          --http=:8080 \
          --harakiri=20 \
          --max-requests=5000 \
          --master \
          --vacuum

EXPOSE 8080
