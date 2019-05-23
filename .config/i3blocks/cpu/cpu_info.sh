#!/bin/sh
TEMP=$(sensors | awk '/Package id 0:/{ printf("%s", $4) }')
USAGE=$(mpstat 1 1 | awk '/:[0-9]{2}.*all/ {printf("%s\n", $4)}')
echo "$USAGE $TEMP" | awk '{ printf(" CPU:%6s% @ %s "), $1, $2 }'
