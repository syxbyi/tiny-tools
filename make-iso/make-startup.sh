#!/bin/bash

sudo fdisk -l
echo
echo "Please choose a device to write: (DO NOT type number after device, like /dev/sdb1)"
read -e device
echo "Please specify an iso file: "
read -e iso
sudo dd bs=4M if="$iso" of="$device" status=progress && sync
