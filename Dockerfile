FROM python:3.5-slim

RUN apt-get update && apt-get install -y \
    postgresql-client libpq-dev \
    gcc gettext \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD src/requirements/requirements.txt ./requirements/requirements.txt
RUN pip install -r requirements/requirements.txt


ADD src/ .
RUN python manage.py compilemessages -v 3

CMD uwsgi --module=blog.base.wsgi \
          --processes=10 \
          --http=:8080 \
          --harakiri=20 \
          --max-requests=5000 \
          --master \
          --vacuum

EXPOSE 8080
