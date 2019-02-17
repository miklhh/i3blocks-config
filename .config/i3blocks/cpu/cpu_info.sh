#!/bin/sh

DIR=$(dirname "$0")
TEMP=$(sensors | egrep "Package id 0:" | awk '{ printf("%s", $4) }')
echo $($DIR/cpu-stat) $TEMP | awk '{ printf(" CPU:%6s% @ %s "), $1, $2 }'
