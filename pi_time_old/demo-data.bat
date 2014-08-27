@echo off
call ..\setup.bat
rem IF EXIST "pi-time.db" DEL "pi-time.db"
python manage.py flush --noinput
python manage.py syncdb --noinput
python demo\test-data.py
