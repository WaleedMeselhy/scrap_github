FROM python:3.7.4-alpine3.10 as base

FROM base as builder
RUN apk update && \
    apk add --virtual .build-deps git \
    gcc \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    musl-dev \
    openssl-dev \
    py3-setuptools \
    linux-headers \
    libc-dev \
    python3-dev && \
    python3 -m ensurepip && \
    pip3 install setuptools
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --install-option="--prefix=/install" --prefer-binary -r /tmp/requirements.txt && \
    rm -r /root/.cache && \
    apk del .build-deps 

FROM base
RUN apk add libxslt
COPY --from=builder /install /usr/local
COPY scrap_github/scrap_github /app/scrap_github
COPY scrap_github/scrapy.cfg /app/scrapy.cfg

WORKDIR /app
ENTRYPOINT [ "sh" ]
ENV PATH="/usr/local/bin:$PATH"

# CMD [ "-c", "scrapy crawl repo_used_by -a repo_name=${repo_name} -o/output/repos.json"]
CMD ["-c","scrapyd-deploy local"]
# CMD ["-c","while true; do echo 'Hit CTRL+C'; sleep 1; done"]