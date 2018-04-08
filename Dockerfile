FROM python:3-alpine
RUN apk update && apk upgrade &&     apk add --no-cache git
WORKDIR /usr/src/app