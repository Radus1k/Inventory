#!/bin/sh
set -e

redis-server /usr/src/redis/redis.conf --loglevel warning

exec "$@"