@echo off
set PYTHONHOME=C:\Python27\
set PYTHONPATH=C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Lib\site-packages;%CD%;
set DJANGO_SETTINGS_MODULE=pi_time.settings
rem IF EXIST "pi-time.db" DEL "pi-time.db"
python manage.py flush --noinput
python manage.py syncdb --noinput
python demo\test-data.py
