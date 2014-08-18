@echo off
set PYTHONHOME=C:\Python27\
set PYTHONPATH=C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Lib\site-packages;%CD%;
set DJANGO_SETTINGS_MODULE=pi_time.settings
python manage.py flush --noinput
python manage.py syncdb
python demo\test-data.py
