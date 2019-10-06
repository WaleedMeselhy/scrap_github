FROM python:3.6-alpine as base 
FROM base as builder

COPY ./requirements.txt /app/requirements.txt
RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add --no-cache postgresql-dev bash && \
    pip install --upgrade cython && \
    pip install --no-cache-dir --user -r /app/requirements.txt && \
    chmod +x /app/entrypoint.sh
COPY ./ /app 
RUN  pip install --no-cache-dir --user  -e /app/core
WORKDIR /app

FROM base
ENV PYTHONUNBUFFERED 1
RUN addgroup -S app && adduser -S -G app app
RUN apk add --no-cache postgresql-dev bash

COPY --chown=app --from=builder /root/.local /usr/local
COPY --chown=app --from=builder /app /app
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/gunicorn.sh

USER app
WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]