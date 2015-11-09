FROM python:2.7-slim

RUN apt-get update && apt-get install -y \
		postgresql-client libpq-dev \
		gcc gettext \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV APP_ROOT=/app \
    APP_VAR_ROOT=/var/blog

ADD src/ $APP_ROOT
WORKDIR $APP_ROOT
VOLUME $APP_VAR_ROOT

RUN pip install -r requirements/requirements.txt && \
    python manage.py compilemessages -v 3

CMD uwsgi --chdir=$APP_ROOT \
          --module=base.wsgi \
          --processes=10 \
          --http=:8080 \
          --harakiri=20 \
          --max-requests=5000 \
          --master \
          --vacuum

EXPOSE 8080
