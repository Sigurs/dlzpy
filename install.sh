#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Add a service account.
useradd -r dlzpy

# Cleanup any old dlzpy files
rm -fR /opt/dlzpy/

# Create a location for the utility
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
# MIGHT EXIST SO BACKUP OLD ONE?
cp -fR $SCRIPT_DIR/configs/alsa/asound.conf /etc/

# Pipewire needs to be restarted to reload alsa config.
# Easiest way is just to kill it.
pkill pipewire -9