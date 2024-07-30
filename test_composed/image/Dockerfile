FROM alpine:latest

RUN apk update
RUN apk add fish

COPY ./*.fish /


ENTRYPOINT [ "/entrypoint.fish" ]
