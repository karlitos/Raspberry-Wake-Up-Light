system settings
===============

This directory contains several configuration files related to various system settings like: WiFi, Real-Time clock ... This configuration files were tested in the Raspbian distribution, other distros may require specific adaptations. 

## interfaces
Contains the network related settings. You have to adapt the "wpa-ssid" and "wpa-psk" so they match yor WiFi configuration.

## modules
The module i2c-dev have to be loaded at the system start, so the i2c bus will be accessible.

## rapsi-blacklist.conf
The "blacklist i2c-bcm2708" has to be commented out, so the i2c module will not be disabled at the system start.

## rc.local
Contains a small script setting the system clock to the right time from the Real-Time clock module. The echo pcf8563 0x51 > /sys/class/i2c-adapter/i2c-0/new_device line has to be adapted to your RTc module and Raspberry-Pi version.
