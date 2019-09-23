#!/bin/bash

# Get directory of script incase of non repository root invocation.
DIR="$(cd "$(dirname "$0")" && pwd)"

# Build targets.
make -C .config/i3blocks/weather

# Ask user for concent.
echo -e "\nAre you sure you want to copy the content of this configuration to \"~/.config/i3blocks\"?"
read -r -p "Any existing configuration in that directory will be overwritten. (y/N)? " answer
case ${answer:0:1} in
    y|Y)
        # Copy files (and remove this script when done).
        cp -v -r "$DIR"/.config ~/;;
    *)
        # Concent not granted.
        echo "No config files have been modified.";;
esac
