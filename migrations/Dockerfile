FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1


# depend on the build.sh script or volume mapping to add the core package
COPY ./migrations/requirements.txt /tmp/requirements.txt
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add --no-cache postgresql-dev bash && \
    pip install --upgrade cython && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY  ./core /app/core
COPY ./migrations /
RUN pip install --no-cache-dir -e /app/core && \
    chmod +x /entrypoint.sh


WORKDIR /migrations

ENV PYTHONPATH=/migrations
ENTRYPOINT ["/entrypoint.sh"]