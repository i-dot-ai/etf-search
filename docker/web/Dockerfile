FROM node:16 as build-stage

ENV TZ=UTC

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./web /app/web

WORKDIR /app/web

RUN npm ci
RUN npm run build

################

FROM python:3.8-buster


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ=UTC

ARG BASE_URL

ENV BASE_URL=${BASE_URL}

WORKDIR /app

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y xvfb xfonts-scalable wkhtmltopdf

RUN python3 -m pip install -U pip setuptools wheel

COPY ./requirements.lock /app/requirements.lock
RUN python3 -m pip install -r /app/requirements.lock --no-cache-dir

COPY ./docker/web/start.sh /start.sh
RUN chmod +x /start.sh

# Set the working directory
WORKDIR /app

COPY . /app

# Copy the app directory and list.txt from build-stage
COPY --from=build-stage /app/web /app/web

RUN \
    DJANGO_SETTINGS_MODULE=etf.settings_base \
    DJANGO_SECRET_KEY="temp" \
    python manage.py collectstatic --no-input

WORKDIR /app/

EXPOSE 8000

CMD ["sh","/start.sh"]
