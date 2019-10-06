FROM python:3.6-alpine as base 
FROM base as builder

COPY ./repo_viewer/requirements.txt /app/requirements.txt
RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add --no-cache postgresql-dev bash && \
    # pip install --upgrade cython && \
    pip install --no-cache-dir --user -r /app/requirements.txt 
COPY  ./core /app/core
COPY ./repo_viewer /app
RUN  pip install --no-cache-dir  --user -e /app/core && \
    chmod +x /app/entrypoint.sh

WORKDIR /app

FROM base
ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache postgresql-dev bash

COPY --from=builder /root/.local /usr/local
COPY --from=builder /app /app
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]