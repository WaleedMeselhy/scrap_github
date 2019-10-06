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



COPY ./scrapper/requirements.txt /tmp/requirements.txt
RUN pip3 install --install-option="--prefix=/install" --prefer-binary --user -r /tmp/requirements.txt
COPY  ./core /app/core
RUN pip3 install --user -e /app/core

FROM base
RUN apk add libxslt postgresql-dev bash
COPY --from=builder /root/.local /usr/local
COPY --from=builder /app /app
COPY ./scrapper/scrap_github/scrap_github /app/scrap_github
COPY ./scrapper/scrap_github/scrapy.cfg /app/scrapy.cfg
COPY ./scrapper/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
WORKDIR /app

ENV PATH="/usr/local/bin:$PATH"
ENTRYPOINT ["/entrypoint.sh"]
CMD ["scrapy crawl repo_used_by -a repo_name=${repo_name} -o/output/repos.json"]
# CMD ["-c","scrapyd-deploy local"]
# CMD ["-c","while true; do echo 'Hit CTRL+C'; sleep 1; done"]