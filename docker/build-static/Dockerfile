FROM node:16 as build-stage

ENV TZ=UTC

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./web /app/web

WORKDIR /app/web

RUN npm ci

CMD ["npm","run","build"]
