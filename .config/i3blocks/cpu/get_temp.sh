#!/bin/sh
sensors | egrep "Package id 0:" | awk '{ printf("%s", $4) }'
