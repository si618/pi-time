from setuptools import setup

setup(
    name = 'pi-time-laptimer',
    version = '0.0.1',
    description = "Pi-time 'laptimer' WAMP Component",
    platforms = ['Any'],
    packages = ['laptimer'],
    include_package_data = True,
    zip_safe = False,
    entry_points = {
        'autobahn.twisted.wamplet': [
            'backend = laptimer.laptimer:LaptimerAppSession'
        ],
    }
)
