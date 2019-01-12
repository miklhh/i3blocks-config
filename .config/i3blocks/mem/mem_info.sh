#!/bin/sh
case $BLOCK_BUTTON in
    1) notify-send "$(ps -axch -o cmd,%mem --sort=-%mem | ~/.config/i3blocks/mem/mem_summarize.py | head | column -t)";;
    3) echo "Right click!";;
esac

echo -e "\U0001F40F" $(free -h | egrep "Mem: ") | awk '{ printf(" %s %s/%s ", $1, $4, $3) }'


