FROM golang:1.21-alpine as builder

ARG SSHPIPERD_VERSION=1.2.3

RUN apk add --no-cache git build-base

ENV CGO_ENABLED=1
ADD sshmux/ /sshmux/
RUN git clone --depth 1 --branch v${SSHPIPERD_VERSION} https://github.com/tg123/sshpiper /sshpiperd
RUN cd /sshmux && go mod tidy && go build -o sshmux
RUN mkdir -p /sshpiperd/out
RUN cd /sshpiperd && git submodule update --init --recursive && go mod tidy && go build -o out ./...

FROM alpine:3.18.4

ARG JUPYTERHUB_VERSION=4.0.2
ARG S6_OVERLAY_VERSION=3.1.6.0

RUN apk add --no-cache \
    python3 \
    py3-pip \
    nodejs \
    npm && \
    npm install -g configurable-http-proxy

RUN python3 -m pip install --no-cache-dir \
    jupyterhub==${JUPYTERHUB_VERSION} \
    dockerspawner \
    jupyterhub-nativeauthenticator \
    sshkey_tools

ADD myauthenticator/ /src/myauthenticator/


RUN mkdir /srv/sshpiperd
COPY --from=builder /sshmux/sshmux /srv/sshpiperd/sshmux
COPY --from=builder /sshpiperd/out/sshpiperd /srv/sshpiperd/sshpiperd
RUN mkdir /etc/ssh/


# add s6-overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

# copy s6 services
COPY services.d/ /etc/services.d/

EXPOSE 8000
EXPOSE 2222

ENV PYTHONPATH=/src
ENV SSHPIPERD_SERVER_KEY_GENERATE_MODE="notexist"

CMD ["/init"]
