#!/bin/sh
echo -e "\U0001F40F" $(free -h | egrep "Mem: ") | awk '{ printf(" %s %s/%s ", $1, $4, $3) }'
