#!/bin/sh

for i in `seq 1 3`;
do
    echo $i
    DISK=$(~/.config/i3blocks/disk/disk_info.sh)                # 1.02 [s]
    BAT=$(~/.config/i3blocks/battery/battery_info.sh)           # 2.26 [s]
    MEM=$(~/.config/i3blocks/mem/mem_info.sh)                   # 0.93 [s]
    SND=$(~/.config/i3blocks/sound/sound_info.sh)               # 1.50 [s]
    DAT=$(date | awk '{ printf(" %s %s %s ", $1, $2, $3) }')    # 0.38 [s]
    TIM=$(date | awk '{ printf(" %s ", $4) }')                  # 0.34 [s]

    ### Total time to run all all programs:
    # ~~ 6.36 [s]
done
