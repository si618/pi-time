from setuptools import setup, find_packages

import pi


setup(
	name='pi-time',
	version=pi.__version__,
	description='Pump track lap timer running on a solar powered Raspberry Pi.',
	author='Simon McKenna',
	author_email='sshnug.si+pi-time@gmail.com',
	url='http://github.com/si618/pi-time',
	packages=find_packages(),
	license='LICENSE.txt'
	include_package_data=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Other Audience',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Framework :: Autobahn',
		'Framework :: Django',
	],
	install_requires=[
		"autobahn == 0.5.14",
		"Django >= 1.5",
		"Django-settings >= 1.3",
	zip_safe=False,
)


# Usage of setup.py:
# $> python setup.py register             # registering package on PYPI
# $> python setup.py build sdist upload   # build, make source dist and upload to PYPI