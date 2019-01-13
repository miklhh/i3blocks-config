#!/bin/sh

# Get the disk info.
DISK_USAGE0=$(df -h / | egrep "/" | awk '{ printf("%4s/%s", $4, $2) }')

# Print the disk info.
FLOOPY_EMOJI=$(echo -e "\U0001F4BE")
echo "" $FLOOPY_EMOJI $DISK_USAGE0 ""
