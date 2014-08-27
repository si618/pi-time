@echo off
call ..\setup.bat
set DJANGO_SETTINGS_MODULE=pi_time.settings
python demo\client.py
