#!/bin/bash

# Get directory of script incase of non repository root invocation.
DIR="$(cd "$(dirname "$0")" && pwd)"

# Ask user for concent.
read -p "Are you sure you want to copy the content of this configuration to \"~/.config/i3block\"? Any existing configuration in that directory will be overwritten. (y/n)? " answer
case ${answer:0:1} in
    y|Y)
        # Copy files (and remove this script when done).
        cp -v -r $DIR/.config ~/;;
    *)
        # Concent not granted.
        echo "No files have been modified.";;
esac
