#!/bin/sh

case $BLOCK_BUTTON in

    1) notify-send "\
 Core voltages:
 --------------
$(sensors | egrep "Core [0-9]:" --color | awk '{ printf(" %s %s   %s \n", $1, $2, $3)}')";;

    3) echo "Right click!";;
esac


DIR=$(dirname "$0")
echo $($DIR/cpu-stat) $($DIR/get_temp.sh) | awk '{ printf(" CPU:%6s% @ %s "), $1, $2 }'
