FROM python:3.9-alpine3.13 as backend
LABEL maintainer="m7011e"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE backend.settings

COPY ./requirements.txt /app/requirements.txt
COPY ./backend /app/backend

WORKDIR /app/backend

EXPOSE 7999

RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev libressl-dev musl-dev libffi-dev

RUN python -m venv /app/py && \
    /app/py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /app/py/bin/pip install -r /app/requirements.txt && \
    apk del .tmp-deps && \
    chmod -R a+x /app

ENV PATH="/app/py/bin:$PATH"

ADD ./scripts/backend_run.sh /app/backend
RUN chmod 755 backend_run.sh 

CMD ["./backend_run.sh"]
