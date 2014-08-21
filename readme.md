# Pi-time

Lap timer running on a solar powered Raspberry Pi.

[![Build Status](https://travis-ci.org/si618/pi-time.svg?branch=master)](https://travis-ci.org/si618/pi-time)&nbsp;[![Latest Version](https://pypip.in/version/pi-time/badge.svg)](https://pypi.python.org/pypi/pi-time/)&nbsp;[![Development Status](https://pypip.in/status/pi-time/badge.svg)](https://pypi.python.org/pypi/pi-time/)

#### Development Status

Still lots of work to do, hardware is working and API is getting there, but most of the web front end code still needs to be written.

## Overview

An active infrared sensor is placed on a [pump track](http://adventuresportsjournal.com/biking/pumpin-an-introduction-to-the-world-of-pump-tracks) or whatever you want timed, with a cable running between the sensor and a Raspberry Pi, detecting when a lap starts or finishes, which is then broadcast to riders and spectators over wifi.

The Raspberry Pi (RPi), acts as a wireless access point, web server and sensor receiver, providing users access to lap data via any modern web browser or TODO: mobile app.

Power for the sensor and RPi comes from batteries recharged from a photovoltaic panel (PV). RPi and the PV panel are housed in an enclosure to provide protection from adverse weather, with an external toggle switch to turn on both the RPi and sensor.

Data is stored on the RPi SD card with backup to an authenticated client or TODO: cloud service.

## Software

#### Design

Client/server push notification for laptimer server using [WebSockets](http://tools.ietf.org/html/rfc6455) and [WAMP](http://wamp.ws). Sensor events also use websockets and are separated from the server app to allow multiple sensors on different platforms (Arduino, Beagleboard, etc.), and because RPi.GPIO code needs to run as root, whereas the laptimer server does not.

#### Requirements

* [autobahn](http://autobahn.ws/python) TODO: fallback for old browsers
* [django](https://docs.djangoproject.com/en/1.5/intro/install/)
* [django-bootstrap-toolkit](https://github.com/dyve/django-bootstrap-toolkit/)
* [django-settings](https://github.com/jqb/django-settings/blob/master/README.rst#installation--setup)
* [jsonpickle](https://github.com/jsonpickle/jsonpickle)
* [python](http://python.org/download/)
* [python-win32api](http://sourceforge.net/projects/pywin32/) (if testing on windows)
* [twisted](https://twistedmatrix.com/trac/)

See [requirements](https://github.com/si618/pi-time/blob/master/requirements.txt) for specific versions, and [travis config](https://github.com/si618/pi-time/blob/master/.travis.yml) for test environments.


#### Recommended

* [pip](http://www.pip-installer.org/en/latest/installing.html) ([windows install](http://stackoverflow.com/a/12476379/44540))
* [python-dev](http://packages.debian.org/wheezy/python-dev)


## Hardware

* RPi (tested on [model b](http://au.element14.com/Raspberry_Pi))
* Compatible USB WiFi & optional antenna
* Power source (tested on [solar charger and battery pack](http://cgi.cottonpickers.plus.com/~cottonpickers/forum/viewtopic.php?f=2&t=474&sid=ec0e5edc2965ab799801f71ed28f6c23))
  * [USB 5V to 12V](http://www.ebay.com.au/itm/271176652645?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649) step up to power 12V sensor.
* Sensor (tested on [active infrared dectector](http://www.ebay.com.au/itm/350771078173?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649))
* Enclosure (tested on IP66 [190x290x140 TIBOX](http://www.ebay.com.au/itm/121133523629?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649) lid width too small so had to dremel and silicon)

## Installation

* [Setup operating system](http://www.raspberrypi.org/downloads)
* [Expand file system](http://elinux.org/RPi_raspi-config#expand_rootfs_-_Expand_root_partition_to_fill_SD_card)
* [Config memory split](http://elinux.org/RPi_raspi-config#memory_split_-_Change_memory_split)
* [Setup wifi access point](http://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/overview)
* [Setup captive portal](http://sirlagz.net/2013/08/23/how-to-captive-portal-on-the-raspberry-pi/)
* [Install pi-time](https://pypi.python.org/pypi/pi-time)

Example setup for RT5370 wifi adapter running as wifi access point with captive portal

    sudo apt-get install hostapd dnsmasq

  */etc/network/interfaces*

    ...
    auto wlan0
    iface wlan0 inet static
      address 10.0.0.1
      netmask 255.255.255.0

  */etc/hostapd/hostapd.conf*

    interface=wlan0
    driver=nl80211
    ctrl_interface=/var/run/hostapd
    ctrl_interface_group=0
    ssid=pi-time
    hw_mode=g
    channel=8
    beacon_int=100
    auth_algs=1
    wmm_enabled=1

  */etc/dnsmasq.conf*

    interface=wlan0
    dhcp-range=10.0.0.10,10.0.0.210,255.255.255.0,12h
    address=/#/10.0.0.1

  */etc/default/ifplugd*

    INTERFACES="eth0"
    HOTPLUG_INTERFACES="eth0"
    ...

  finally restart both *hostapd* and *dnsmasq*

    sudo /etc/init.d/hostapd restart
    sudo /etc/init.d/dnsmasq restart

## Diagnostics

LEDs mounted to the enclosure are used to show:
* When the PV is charging batteries (Green via PV panel)
* When the RPi is on (Red via GPIO 3.3V to 0V)
* When the app is running (Blue via GPIO port))
* When a rider is on an active lap (White via GPIO port)

TODO: Add ability to query app log

## Issues

_Issue_:  Only one rider can be on the track at any one time.
_Fix_: Use [radio tags](https://en.wikipedia.org/wiki/Transponder_timing) passing a decoder instead of using an infrared sensor.

_Issue_:  Possible to shortcut tracks which cross over.
_Fix_: Add sensors at key points in the track which have to be triggered before the lap counts as finished. Could also be used for sectors and split times.

_Issue_ : Lap start and finish must be from the same sensor location.
_Fix_: Similar to shortcut issue, add sensors to allow different start and finish locations. Would be good to have automated discovery, so each sensor looks for the lap timer server on the network.

### Hardware Improvements

* Cheaper to use 12v deep cycle lead acid battery instead of AA or D batteries. No converter required for 12v sensor.
* PV panels should be optional (possible with prototype but fairly tightly coupled)
* Cheaper enclosure by using metal or plastic box and appropriate use of silicon.
* Wifi, wireless mesh, 3/4G, satellite etc. could be used to send sensor events back to the laptimer server. TLS or similar encryption required as well as sensor authentication.

### Software Improvements

* Provide option to connect to existing WiFi access point instead of RPi, use RPi access point as fallback.
* Add chat for riders, spectators and admin (different permissions, broadcast ability, etc.).
* Instead of just timing laps, add scoring system (for slopestyle, dirt jams, etc.) which is broadcast like lap times.
