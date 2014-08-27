from setuptools import setup

setup(
    name = 'pi-time-sensor',
    version = '0.0.1',
    description = "Pi-time 'sensor' WAMP Component",
    platforms = ['Any'],
    packages = ['sensor'],
    include_package_data = True,
    zip_safe = False,
    entry_points = {
        'autobahn.twisted.wamplet': [
            'backend = sensor.sensor:AppSession'
        ],
    }
)
