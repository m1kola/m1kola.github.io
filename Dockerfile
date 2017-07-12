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

# We need to include compiled messages into a Docker image.
# SECRET_KEY is actually not so important for compilemessages,
# but Django now requires this to run compilemessages.
RUN CFG_SECRET_KEY=fake_build_key python manage.py compilemessages -v 3

CMD uwsgi --module=wsgi \
          --processes=10 \
          --http=:8080 \
          --harakiri=20 \
          --max-requests=5000 \
          --master \
          --vacuum

EXPOSE 8080
