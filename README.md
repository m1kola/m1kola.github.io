# mikola.by

Wagtail build of [mikola.by](http://mikola.by)

## How to run the project locally

To run the project locally you need to install Docker.

When you have Docker installed, you can execute the following command to run the project:

```
docker-compose -f docker-compose.dev.yml up -d
```

On the first run you need to execute the following commands:

```
docker-compose run --rm blog_app ./manage.py migrate
docker-compose run --rm blog_app ./manage.py createsuperuser
docker-compose restart blog_app
```
