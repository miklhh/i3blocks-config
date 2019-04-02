#!/bin/sh
TEMP=$(sensors | awk '/Package id 0:/{ printf("%s", $4) }')
USAGE=$(~/.config/i3blocks/cpu/cpu-stat)
echo $USAGE $TEMP | awk '{ printf(" CPU:%6s% @ %s "), $1, $2 }'
