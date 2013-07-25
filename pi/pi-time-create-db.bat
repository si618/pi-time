@echo off
IF EXIST "pi-time.db" DEL "pi-time.db"
python manage.py syncdb --noinput
python manage.py loaddata "pi-time-test-data.json"
