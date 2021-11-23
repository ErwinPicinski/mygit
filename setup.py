#! /usr/bin/env python3

from setuptools import setup


setup(name = 'mygit',
      version = '1.0',
      description='Basic implementation of git',
      author='Erwin Picinski',
      packages=['mygit'],
      entry_points={
          'console_scripts' : [
              'mygit = mygit.main:main'
              ]
      })