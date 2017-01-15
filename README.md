# mikola.by

Wagtail build of [mikola.by](http://mikola.by)

## How to run the project locally

To run the project locally you need to install Docker.

When you have Docker installed, you can execute the following command to run the project:

```
docker-compose -f docker-compose.dev.yml up -d
```

After the first run, you will need to execute the following commands:

```
docker-compose -f docker-compose.dev.yml run --rm blog_app ./manage.py migrate
docker-compose -f docker-compose.dev.yml run --rm blog_app ./manage.py createsuperuser
docker-compose -f docker-compose.dev.yml restart blog_app
```

Now you can open [http://localhost:8000](http://localhost:8000/)

### Front-end

The project uses [Gulp tasks](https://github.com/m1kola/mikola.by/tree/master/src/gulpfile.js) and [npm scripts](https://github.com/m1kola/mikola.by/blob/master/src/package.json) to build static. Normally you don't need to run any npm scripts when you use the `docker-compose.dev.yml` config. Docker will run the `npm run watch` command in a container.

If you want to follow the output of the command you can run this command:

```
docker-compose -f docker-compose.dev.yml logs -f blog_app_frontend
```

To stop a container with the `npm run watch` script, run:

```
docker-compose -f docker-compose.dev.yml stop blog_app_frontend
```
