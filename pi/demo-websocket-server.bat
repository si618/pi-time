@echo off
set PYTHONHOME=C:\Python27\
set PYTHONPATH=C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Lib\site-packages;%CD%;
set DJANGO_SETTINGS_MODULE=pi.settings
python demo\websocket.server.py