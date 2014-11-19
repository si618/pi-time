# Pi-time

Lap timer running on a solar powered Raspberry Pi.

[![Build Status](https://travis-ci.org/si618/pi-time.svg?branch=master)](https://travis-ci.org/si618/pi-time)&nbsp;[![Latest Version](https://pypip.in/version/pi-time/badge.svg)](https://pypi.python.org/pypi/pi-time/)&nbsp;[![Development Status](https://pypip.in/status/pi-time/badge.svg)](https://pypi.python.org/pypi/pi-time/)

#### Development Status

Still lots of work to do, hardware prototype is working and API is getting there, but most of the web front end code still needs to be written.

## Overview

An active infrared sensor is placed on a [pump track](http://adventuresportsjournal.com/biking/pumpin-an-introduction-to-the-world-of-pump-tracks), or whatever activity needs timing, with a cable running between the sensor and a Raspberry Pi, detecting when a lap starts or finishes, which is then broadcast to riders and spectators over wifi.

The Raspberry Pi (RPi), or any hardware capable of running python and networking, acts as a wireless access point, web server and sensor receiver, providing users access to lap data via any modern web browser.

Power for the sensor and RPi comes from batteries recharged from a photovoltaic panel (PV). RPi and the PV panel are housed in an enclosure to provide protection from adverse weather, with an external switch to turn on both the RPi and sensor. Data is stored on the RPi SD card with backup to an authenticated client or cloud service.

Need more information?  Feel free to ask in the [web forum](https://groups.google.com/forum/#!forum/pi-time).  

## Software

#### Design

Pi-time is built upon the [Crossbar](http://crossbar.io/) platform, which uses [WebSockets](http://tools.ietf.org/html/rfc6455) and [WAMP](http://wamp.ws). A crossbar application is used as the application and web [server](https://github.com/si618/pi-time/tree/master/pi_time/laptimer), pushing out notifications of events in near real-time as they are received from [sensors](https://github.com/si618/pi-time/tree/master/pi_time/sensor) which are separate crossbar applications, or users from a web browser or mobile app. A single Raspberry Pi can be used to run both the laptimer server and sensor application, although the design allows for multiple sensors to be connected.

As there are many different types of activities that can benefit from the use of timers, pi-time is designed to allow different activities to be added as needed, and is not restricted to a particular hardware platform, although it is being built using a 'mobile first' approach, so assumes that users will interact with the software via a mobile device.  

#### Requirements

* [python](http://python.org/download/)
* [python-win32api](http://sourceforge.net/projects/pywin32/) (if using on windows o/s)
* [pip](http://www.pip-installer.org/en/latest/installing.html) ([windows install](http://stackoverflow.com/a/12476379/44540))

## Hardware

* RPi (tested on [model b](http://au.element14.com/Raspberry_Pi))
* Compatible USB WiFi & optional antenna
* Power source (tested on [solar charger and battery pack](http://cgi.cottonpickers.plus.com/~cottonpickers/forum/viewtopic.php?f=2&t=474&sid=ec0e5edc2965ab799801f71ed28f6c23))
  * [USB 5V to 12V](http://www.ebay.com.au/itm/271176652645?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649) step up to power 12V sensor.
* Sensor (tested on [active infrared detector](http://www.ebay.com.au/itm/350771078173?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649))
* Enclosure (tested on IP66 [190x290x140 TIBOX](http://www.ebay.com.au/itm/121133523629?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649) lid width too small so had to dremel and silicon)

## Installation

* [Setup operating system](http://www.raspberrypi.org/downloads)
* [Expand file system](http://elinux.org/RPi_raspi-config#expand_rootfs_-_Expand_root_partition_to_fill_SD_card)
* [Config memory split](http://elinux.org/RPi_raspi-config#memory_split_-_Change_memory_split)
* [Setup wifi access point](http://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/overview) (optional, could connect via ethernet)
* [Setup captive portal](http://sirlagz.net/2013/08/23/how-to-captive-portal-on-the-raspberry-pi/) (optional, could use existing wifi network)
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

### Development

#### Setting up a development environment:

* [Install git](http://git-scm.com/downloads)
* [Clone pi-time](https://github.com/si618/pi-time.git)
* [Install python](#Requirements)
* [Install python-dev](http://packages.debian.org/wheezy/python-dev)
* [Install node.js](http://nodejs.org/download/) (also installs NPM)
* [Install grunt](http://gruntjs.com/getting-started)
* [Install bower](http://bower.io/#install-bower)

#### Dependency management

[PIP](http://www.pip-installer.org) is used for python packages.

[NPM](https://www.npmjs.org/) is used for developer modules (unit tests, linting, ...).

[Bower](http://bower.io/) is used for web front-end components (jquery, knockout, ...).

#### Workflow

[Grunt](http://gruntjs.com/) manages build, test and release processes. Run `grunt --help` for available tasks and see [Gruntfile.js](https://github.com/si618/pi-time/blob/master/Gruntfile.js) for configuration.

[Travis]((https://travis-ci.org/si618/pi-time)) provides continuous integration. See [travis config](https://github.com/si618/pi-time/blob/master/.travis.yml) for test environments.

Run `python requirements.py` to update all PIP, NPM and Bower dependencies.   

Pi-time uses the [Bootstrap](http://getbootstrap.com/) web framework, along with a customised version of a [Bootswatch](http://bootswatch.com/slate) theme.
When new releases of bootstrap or bootswatch are available, currently the bootstrap css must be manually recompiled by copying the variables.less from pi-time to a clone of bootswatch, running `grunt swatch:slate` then copying the bootstrap css back to pi-time. Hopefully this will get automated (via bower?) in the future.  
