@echo off
..\setup.bat
set DJANGO_SETTINGS_MODULE=pi_time.settings
rem IF EXIST "pi-time.db" DEL "pi-time.db"
python manage.py flush --noinput
python manage.py syncdb --noinput
python demo\test-data.py
