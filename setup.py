# -*- coding: utf-8 -*-


'''setup.py: setuptools control.'''

import re
from setuptools import setup, find_packages

with open('assembla/__init__.py') as f:
    version = re.search('^__version__\s*=\s*\'(.*)\'', f.read(), re.M).group(1)


with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8')


setup(name='assembla-cli',
      version=version,
      description='A small command-line tool for working with Assembla spaces',
      long_description=long_description,
      author='Michael Spencer',
      author_email='sonrisesoftware@gmail.com',
      url='https://github.com/iBeliever/assembla-cli',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'Click',
      ],
      entry_points='''
          [console_scripts]
          assembla=assembla.main:cli
      ''')
