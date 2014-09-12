@echo off
rem Hint: To cleanly breakout of this script, hit CTRL+C twice
set PYTHONHOME=C:\Python27\
set PYTHONPATH=C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Lib\site-packages;%~dp0dist\laptimer\pi_time
cd dist\laptimer\pi_time\laptimer
crossbar start --loglevel debug
cd ..\..\..\..\