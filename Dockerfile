FROM python:3.12.0-alpine3.18

# hadolint ignore=DL3018
RUN apk add --update --no-cache bash ca-certificates curl git jq openssh

COPY ["src/requirements.txt", "/src/"]

# hadolint ignore=DL3013
RUN pip install --no-cache-dir -r /src/requirements.txt

RUN ["bin/sh", "-c", "mkdir -p /src"]

COPY ["src", "/src/"]

ENTRYPOINT ["/src/entrypoint.sh"]
