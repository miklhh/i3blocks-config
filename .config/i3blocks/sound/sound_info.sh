#!/bin/sh

MUTE="🔇"
LOW="🔈"
MID="🔉"
HIGH="🔊"

SOUND_LEVEL=$(amixer get Master | awk -F"[][]" '/%/ { print $2 }' | awk -F"%" 'BEGIN{tot=0; i=0} {i++; tot+=$1} END{printf("%s\n", tot/i) }')
MUTED=$(amixer get Master | awk ' /%/{print ($NF=="[off]" ? 1 : 0); exit;}')

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

echo $ICON $SOUND_LEVEL | awk '{ printf(" %s:%3s%% \n", $1, $2) }'
