# base
FROM ubuntu:24.04 AS base

ARG HTTP_PROXY=""
ARG HTTPS_PROXY=""

SHELL [ "/usr/bin/env", "bash", "-c" ]
ENV DEBIAN_FRONTEND=noninteractive
ENV HTTP_PROXY ${HTTP_PROXY}
ENV HTTPS_PROXY ${HTTPS_PROXY}}

RUN apt update
RUN apt install -y nano less
RUN apt install -y python3
RUN apt install -y python3-pip python3-venv


ENTRYPOINT [ "bash" ]



# build-wheel
FROM base AS build-wheel

RUN apt install -y python3-build

WORKDIR /wheel

COPY ./src ./src
COPY ./LICENSE.md ./
COPY ./README.md ./
COPY ./pyproject.toml ./

RUN python3 -m build



# install-wheel
FROM base AS install-wheel

WORKDIR /opt
RUN python3 -m venv container-health-exporter

WORKDIR /opt/container-health-exporter
COPY --from=build-wheel /wheel/dist/*.whl /tmp/wheel/
RUN source ./bin/activate \
    && pip install /tmp/wheel/container_health_exporter-*-py3-none-any.whl \
    && deactivate



# make-deb
FROM base as make-deb

RUN apt install -y build-essential
RUN apt install -y debhelper dh-python

WORKDIR /work/source
COPY ./debian ./debian

COPY --from=install-wheel /opt/container-health-exporter ./container-health-exporter

RUN dpkg-buildpackage -us -uc -b



# copy-deb
FROM base AS copy-deb

COPY ./builder/copy_deb_entrypoint.bash /entrypoint.bash

WORKDIR /work
COPY --from=make-deb /work/*.deb /work


ENTRYPOINT [ "/entrypoint.bash" ]