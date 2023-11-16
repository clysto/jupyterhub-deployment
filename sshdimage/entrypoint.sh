#!/bin/sh

exec /sshpiperd/sshpiperd --drop-hostkeys-message /sshpiperd/splice --template $TEMPLATE
