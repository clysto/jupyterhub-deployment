FROM alpine:3.18.4

# Add user nobody with id 1
ARG USERID=1000
ARG GROUPID=1000
RUN addgroup -g $GROUPID -S sshpiperd && adduser -u $USERID -S sshpiperd -G sshpiperd

RUN mkdir -p /sshpiperd
ADD entrypoint.sh /sshpiperd
RUN mkdir /etc/ssh/

# Add execution rwx to user 1
RUN chown -R $USERID:$GROUPID /etc/ssh/

COPY ./bin/sshpiperd ./bin/splice /sshpiperd/
USER $USERID:$GROUPID
EXPOSE 2222

ENV TEMPLATE="example.com"
ENV SSHPIPERD_SERVER_KEY_GENERATE_MODE="notexist"

ENTRYPOINT [ "/sshpiperd/entrypoint.sh" ]
