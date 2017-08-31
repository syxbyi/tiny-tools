#!/bin/bash

echo "Select target iso file: "
read -e iso
sudo mount -o loop "$iso" /mnt/cdrom
cd /mnt/cdrom
./install
