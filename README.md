# Pi-time

Pump track lap timer running on a solar powered Raspberry Pi with battery backup.

## Overview

An active infrared sensor is placed at a suitable point on a [pump track](http://adventuresportsjournal.com/biking/pumpin-an-introduction-to-the-world-of-pump-tracks), a cable runs between the sensors and a Raspberry Pi (RPi) providing data to trigger when a lap starts or finishes.

A python application runs on the RPi listening to the sensor, recording lap times as well as information on the track, the current session and rider.

RPi acts as both a wireless access point and web server, allowing authenticateds user to use the application via a web browser or mobile app.

Power for the sensor and RPi comes from batteries recharged from a photovoltaic panel (PV). RPi and PV panel are housed in an enclosure to provide protection from adverse weather, with an external toggle switch to turn on both the RPi and sensor. 

Data is stored on the RPi SD card with the option to backup all data to an authenticated client.

## Software

#### Required

* [python](http://python.org/download/) (tested on 2.7)
* [django](https://docs.djangoproject.com/en/1.5/intro/install/) (tested on 1.5)
* [django-settings](https://github.com/jqb/django-settings/blob/master/README.rst#installation--setup) (tested on 1.3-3 beta)

#### Undecided

* [djangorestframework](http://django-rest-framework.org/#installation) (testing 2.3.6) vs [autobahn.ws] (http://autobahn.ws/python) (testing 0.5.14) - probably need fallback for old browsers if using websockets...

#### Recommended

* [raspbian](http://www.raspberrypi.org/downloads) (tested on wheezy)
* [python-dev](http://packages.debian.org/wheezy/python-dev)
* [pip](http://www.pip-installer.org/en/latest/installing.html) ([windows install](http://stackoverflow.com/a/12476379/44540)) (tested on 1.5)


## Hardware

* RPi (tested on [model b](http://au.element14.com/Raspberry_Pi))
* USB WiFi & optional antenna (ensure compatible with RPi and can run as access point)
* Power source (tested on [solar charger and battery pack](http://cgi.cottonpickers.plus.com/~cottonpickers/forum/viewtopic.php?f=2&t=474&sid=ec0e5edc2965ab799801f71ed28f6c23))
  * [USB 5V to 12V](http://www.ebay.com.au/itm/271176652645?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649) step up to power 12V sensor.
* Sensor (tested on [active infrared dectector](http://www.ebay.com.au/itm/350771078173?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649))
* Enclosure (tested on IP66 [190x290x140 TIBOX](http://www.ebay.com.au/itm/121133523629?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649) lid width too small so had to dremel and silicon)

## Installation

TODO - Detail setup of 

## Diagnostics

LEDs mounted to the enclosure are used to show:
* When the PV is charging (Green via PV Panel)
* When the RPi is on (Red via GPIO 3.3V to 0V)
* When the app is running (Blue via GPIO port, solid = ok, flashing = problem)
* When a rider is on an active lap (White via GPIO port)

TODO - Add ability to query app log


## Issues

_Problem_:  Only one rider can be on the track at any one time.  
_Solution_: Use radio tags on bikes passing a receiver instead of using an infrared sensor.

_Problem_:  Possible to shortcut tracks which cross over.  
_Solution_: Add beacons at key points in the track which have to be triggered before the lap counts as finished.

## Improvements to prototype

* Cheaper to use 12v lead acid battery instead of AA or D batteries. No converter required for 12v sensor.
* PV panels should be optional (possible with prototype but fairly tightly coupled)
* Cheaper enclosure by using metal or plastic box and appropriate use of silicon.
* Provide option to connect to existing WiFi access point instead with RPi access point as fallback.
