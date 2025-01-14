FROM oven/bun:latest as static_files
WORKDIR /code
ENV PATH /code/node_modules/.bin:$PATH
COPY package.json bun.lockb /code/
RUN bun install
COPY . /code/
RUN bun run build
RUN bun run build:css

FROM python:3.12.6-slim-bookworm as base

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    build-essential \
    libpcre3 \
    curl \
    gnupg2 \
    vim \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null \
    && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" > /etc/apt/sources.list.d/postgresql.list' \
    && apt-get update && apt-get install -y --no-install-recommends postgresql-client-{{ cookiecutter.postgres_version }} \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
ADD . /code/
# Add uv to install requirements

COPY --from=ghcr.io/astral-sh/uv:0.5.1 /uv /bin/uv
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN uv sync --frozen --no-dev --group prod

COPY --from=static_files /code/{{ cookiecutter.project_app }}/static /code/{{ cookiecutter.project_app }}/static

FROM base AS deploy

# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# uWSGI will listen on this port
EXPOSE 8000

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE={{ cookiecutter.project_app }}.settings.deploy

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DATABASE_URL='' ENVIRONMENT='' DJANGO_SECRET_KEY='dummy' DOMAIN='' python manage.py collectstatic --noinput -i *.scss --no-default-ignore

## Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE={{ cookiecutter.project_app }}/wsgi.py

## Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy UWSGI_IGNORE_SIGPIPE=true UWSGI_IGNORE_WRITE_ERRORS=true UWSGI_DISABLE_WRITE_EXCEPTION=true

# Number of Granian workers and threads per worker (customize as needed):
# ENV GRANIAN_WORKERS=2 GRANIAN_THREADS=4

## uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/code/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Start uWSGI
CMD ["uwsgi", "--single-interpreter", "--enable-threads", "--show-config"]

