FROM python:3.9-stretch


#Basic S.O Libs
RUN apt-get update && apt-get install -y
RUN apt-get install -y --no-install-recommends gettext libcairo2 libffi-dev libpango1.0-0 \
  libgdk-pixbuf2.0-0 libxml2-dev libxslt1-dev shared-mime-info

# Required envs
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=settings \
    TZ=America/Sao_Paulo \
    OAUTHLIB_INSECURE_TRANSPORT=False \
    PYTHONPATH=sec\
    DEBUG=false

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /usr/src/app

# CMD gunicorn    --bind 0.0.0.0:8000      \
#                 --reload wsgi:application
CMD python manage.py runserver 0.0.0.0:80