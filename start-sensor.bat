@echo off
set PYTHONHOME=C:\Python27\
set PYTHONPATH=C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Lib\site-packages;%~dp0dist\sensor\pi_time
cd dist\sensor\pi_time\sensor
crossbar start --loglevel debug
cd ..\..\..\..\