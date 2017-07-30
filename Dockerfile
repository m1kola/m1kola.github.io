# Build front-end
FROM node:6.5 AS assets

WORKDIR /app

# Install node packages. Done in a separate step so Docker can cache it.
COPY src/package.json .
RUN npm install

# Configure gulp to build static assets to this dir
ENV CFG_STATIC_COMPILED_DIR /app/static_compiled

# Copy sources, so we would be able to compile static.
COPY src/ .
RUN npm run build


# Build back-end
FROM python:3.6-slim

# Install non-python dependencies
RUN apt-get update && apt-get install -y \
    gcc postgresql-client libpq-dev \
    # Django needs gettext to be able to work with translations
    gettext \
    # Wagtail needs libjpeg to be able to work with images
    libjpeg62-turbo-dev \
    # uWSGI needs mime-support to serve static files
    # with the correct content-type header
    mime-support \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python packages. Done in a separate step so Docker can cache it.
COPY src/requirements/requirements.txt ./requirements/requirements.txt
RUN pip install -r requirements/requirements.txt

# Copy a script to run the application.
COPY bin/run.sh /run.sh
CMD ["/run.sh"]

# Copy sources, so we would be able to run the application.
COPY src/ .

# Copy static assets from the previous stage
COPY --from=assets /app/static_compiled /app/static_compiled

# We need to include compiled messages and static fields into a Docker image.
# SECRET_KEY is actually not so important for compilemessages and collectstatic,
# but Django now requires this to run these commands.
RUN CFG_SECRET_KEY=fake python manage.py compilemessages -v 3
RUN CFG_SECRET_KEY=fake python manage.py collectstatic --noinput


EXPOSE 8080
