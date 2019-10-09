FROM python:3.7.4-alpine3.10 as base

FROM base as builder
RUN apk update && \
    apk add git \
    gcc \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    musl-dev \
    openssl-dev \
    py3-setuptools \
    linux-headers \
    libc-dev \
    postgresql-dev \
    python3-dev && \
    python3 -m ensurepip && \
    pip3 install setuptools

COPY ./scrapyd/requirements.txt /tmp/requirements.txt
RUN pip3 install --install-option="--prefix=/install" --prefer-binary -r /tmp/requirements.txt

COPY  ./core /app/core
RUN pip3 install --user /app/core


FROM base
RUN apk add libxslt postgresql-dev bash
COPY --from=builder /install /usr/local
COPY --from=builder /root/.local /usr/local

ENV PATH="/usr/local/bin:$PATH"
COPY ./scrapyd/scrapyd.conf /etc/scrapyd/
COPY ./scrapper/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 6800

ENTRYPOINT ["/entrypoint.sh"]
CMD ["scrapyd", "--pidfile="]
