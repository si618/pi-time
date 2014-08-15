from setuptools import setup, \
					   find_packages
import pi_time


setup(
	name='pi-time',
	version=pi_time.__version__,
	description='Pump track lap timer running on a solar powered Raspberry Pi.',
	author=pi_time.__author__,
	author_email='sshnug.si+pi-time@gmail.com',
	url='http://github.com/si618/pi-time',
	packages=find_packages(),
	license='GNU General Public License v3 or later (GPLv3+)',
	include_package_data=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Other Audience',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Framework :: Django',
	],
	install_requires=open('requirements.txt').read(),	
	zip_safe=False,
)


# Usage of setup.py:
# $> python setup.py register             # registering package on PYPI
# $> python setup.py build sdist upload   # build, make source dist and upload to PYPI