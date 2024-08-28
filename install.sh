#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Cleanup any old installation files
rm -fR /opt/dlzpy/*

# Add a service account.
useradd -r dlzpy -d /opt/dlzpy

# Make sure we have a location for the utility
mkdir /opt/dlzpy

# Copy files over to installation dir
cp -fR $SCRIPT_DIR /opt/

# Cleanup any possible development artifacts
rm -fR /opt/dlzpy/.venv /opt/dlzpy/.idea/

# Give dlzpy permissions to it's installation folder
chown -R dlzpy:dlzpy /opt/dlzpy/

# Setup the python venv by creating it and installing required packages.
sudo -u dlzpy /opt/dlzpy/scripts/setup-venv.sh

# Copy udev rule
cp -fR $SCRIPT_DIR/configs/udev/60-dlzpy.rules /etc/udev/rules.d/

# Copy asound.conf
cp -fR $SCRIPT_DIR/configs/alsa/asound.conf /etc/

if [ -e "/etc/asound.conf" ]; then
    echo "/etc/asound.conf already exists! Please merge $SCRIPT_DIR/configs/alsa/asound.conf with your existing file."
else
  cp -fR $SCRIPT_DIR/configs/alsa/asound.conf /etc/
fi

# Trying to avoid the need for a reboot.
## Reload udev rules
udevadm control --reload-rules

## Pipewire needs to be restarted to reload alsa config.
## Easiest way is just to kill it.
pkill pipewire -9
