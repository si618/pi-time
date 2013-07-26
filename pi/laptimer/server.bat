@echo off
set PYTHONHOME=C:\Python27\;%CD%;
set PYTHONPATH=C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Lib\site-packages;
set DJANGO_SETTINGS_MODULE=pi.settings
python server.py