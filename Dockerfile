FROM python:3.9-slim
LABEL INCREMENTMEWHENSTUCK=1
ENV PYTHONUNBUFFERED 1

RUN set -ex \
    && buildDeps=' \
    build-essential \
    curl \
    wget \
    ' \
    && deps=' \
    libexpat1 \
    python-pygraphviz \
    postgresql-client \
    ca-certificates \
    git \
    ' \
    && apt-get update && apt-get upgrade -y && apt-get install -y $buildDeps $deps --no-install-recommends  && rm -rf /var/lib/apt/lists/*\
    && pip install uwsgi \
    && apt-get purge -y --auto-remove $buildDeps \
    && find /usr/local -depth \
    \( \
    \( -type d -a -name test -o -name tests \) \
    -o \
    \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    \) -exec rm -rf '{}' +

RUN pip install pipenv && pip install uwsgi

RUN mkdir /code
WORKDIR /code
ADD . /code/

COPY Pipfile /code
COPY Pipfile.lock /code
RUN  pipenv lock -r > requirements.txt
# COPY requirements.txt /code/

RUN pip install -r requirements.txt


# uWSGI will listen on this port
EXPOSE 8000

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DATABASE_URL="postgres://nonexistence:5432/none" python manage.py collectstatic --noinput

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE="thairod/wsgi.py"

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=1 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/code/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Deny invalid hosts before they get to Django (uncomment and change to your hostname(s)):
# ENV UWSGI_ROUTE_HOST="^(?!localhost:8000$) break:400"

# Uncomment after creating your docker-entrypoint.sh
# ENTRYPOINT ["/code/docker-entrypoint.sh"]

RUN chmod +x /code/docker-entrypoint.sh

# Start uWSGI
ENTRYPOINT ["/code/docker-entrypoint.sh"]

CMD ["uwsgi", "--show-config"]
