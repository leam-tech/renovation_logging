# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in renovation_logging/__init__.py
from renovation_logging import __version__ as version

setup(
	name='renovation_logging',
	version=version,
	description='Log Server for all the sites',
	author='Leam Technology Systems',
	author_email='admin@leam.ae',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
