# Make startup devices

Run command:

```sh
./make-startup.sh
```

The main codes in this script is:

```sh
sudo dd bs=4M if="$iso" of="$device" status=progress && sync
```

# Install Linux iso file to portable devices

Run command:

```sh
./linux-to-usb.sh
```

The main codes is:

```sh
sudo mount -o loop "$iso" /mnt/cdrom
./install
```

Reference: [Linux下打开ISO文件两种方法](http://www.onesl.com/web/smkj/2011040505.html)
