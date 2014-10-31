"""PYPI configuration for laptimer sensor."""
from setuptools import setup

setup(
    name="pi-time-sensor",
    version="0.0.1",
    description="WAMP component for pi-time sensor",
    platforms=["Any"],
    packages=["sensor"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "autobahn.twisted.wamplet": [
            "backend = sensor.sensor:SensorAppSession"
        ],
    }
)
