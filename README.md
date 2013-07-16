# pi-time

Pump track lap timer running on a solar powered Raspberry Pi.

## Software

#### Required

* [python](http://python.org/download/) (tested on 2.7)
* [django](https://docs.djangoproject.com/en/1.5/intro/install/) (tested on 1.5)
* [django-settings](https://github.com/jqb/django-settings/blob/master/README.rst#installation--setup) (tested on 1.3-2 beta)
* [djangorestframework](http://django-rest-framework.org/#installation) (tested on 2.3.6)

#### Recommended

* [pip](http://www.pip-installer.org/en/latest/installing.html) ([install on windows](http://stackoverflow.com/a/12476379/44540)) (tested on 1.5)

## Hardware

* Raspberry Pi (tested on [512MB Model B](http://au.element14.com/Raspberry_Pi))
* Power source (tested on [solar charger and battery pack](http://cgi.cottonpickers.plus.com/~cottonpickers/forum/viewtopic.php?f=2&t=474&sid=ec0e5edc2965ab799801f71ed28f6c23))
  * [USB 5V to 12V](http://www.ebay.com.au/itm/271176652645?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649) step up to power 12V sensor.
  * [4 x AA to D](http://www.ebay.com.au/itm/281077247363?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649) adapters, simply because we have lots of AA rechargables, and no D size.
* Sensor (tested on [active infrared dectector](http://www.ebay.com.au/itm/350771078173?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649))
* Enclosure (tested on IP66 [190x290x140 TIBOX](http://www.ebay.com.au/itm/121133523629?ssPageName=STRK:MEWNX:IT&_trksid=p3984.m1497.l2649) but lid width was just too small so had to dremel and silicon)
 