#!/bin/sh

# If ACPI was not installed, this probably is a battery-less computer.
ACPI_RES=$(acpi)
if [ $? -eq 0 ]
then
    echo -e "\U0001F50B" "\u23F3" $ACPI_RES | awk '{ printf("%s%s: %s%s ", $1, substr($6, 1, length($6) - 1), $2, substr($7, 0, 5)) }'
fi
