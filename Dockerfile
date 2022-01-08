FROM python:3.9.9-alpine3.15 as backend
LABEL maintainer="m7011e"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE backend.settings

COPY requirements.txt /requirements.txt
COPY backend /backend
COPY scripts /scripts

WORKDIR /backend
EXPOSE 7999

RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev libressl-dev musl-dev libffi-dev
ENV LIBRARY_PATH=/lib:/usr/lib

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chmod -R +x /scripts


ENV PATH="/scripts:/py/bin:$PATH"

CMD["run.sh"]