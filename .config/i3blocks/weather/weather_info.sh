#!/bin/sh

case $BLOCK_BUTTON in
    1) notify-send "$(curl wttr.in/Linköping | sed -r "s/\x1B\[([0-9]{1,3}((;[0-9]{1,3})*)?)?[m|K]//g")";;
    3) notify-send " $(~/.config/i3blocks/weather/weather.py 5) "
esac

echo "" $(~/.config/i3blocks/weather/weather.py 1 2) ""
