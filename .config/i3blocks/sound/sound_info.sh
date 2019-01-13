#!/bin/sh

MUTE=$(echo -e "\U0001F507")
LOW=$(echo -e "\U0001F508")
MID=$(echo -e "\U0001F509")
HIGH=$(echo -e "\U0001F50A")

AMIXER=$(amixer get Master | grep "%")
SOUND_LEVEL=$(echo $AMIXER | awk '{ printf("%s", substr($4, 2, length($4) -3)) }')
MUTED=$(echo $AMIXER | awk '{ printf("%d", ($6 == "[off]" ? 1 : 0)) }')
ICON=$MUTE

if [ $MUTED = "1" ]
then
    ICON=$MUTE
elif [ $SOUND_LEVEL -lt 34 ]
then
    ICON=$LOW
elif [ $SOUND_LEVEL -lt 67 ]
then
    ICON=$MID
else
    ICON=$HIGH
fi

echo "" $ICON $SOUND_LEVEL | awk '{ printf(" %s:%3s\% \n", $1, $2) }'
