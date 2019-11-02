#!/bin/sh
TEMP=$(sensors | awk '/Package id 0:/{ printf("%s\n", $4) }')
CPU_USAGE=$(mpstat 1 1 | awk '/Average:/ {printf("%s\n", $(NF-9))}')
echo "$CPU_USAGE $TEMP" | awk '{ printf(" CPU:%6s% @ %s \n"), $1, $2 }'
