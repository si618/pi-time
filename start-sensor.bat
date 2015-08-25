@echo off
rem Hint: To cleanly breakout of this script, hit CTRL+C twice
set PYTHONHOME=C:\tools\python2\
set PYTHONPATH=C:\tools\python2\Lib;C:\tools\python2\DLLs;C:\tools\python2\Lib\site-packages;%~dp0dist\sensor\pi_time
cd dist\sensor\pi_time\sensor
crossbar start --loglevel debug
cd ..\..\..\..\