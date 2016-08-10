#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'JobBot',
    'author': 'Andrew McRobb',
    'url': 'URL to get it at.',
    'download_url': '',
    'author_email': 'andrewmcrobb@gmail.com',
    'version': '0.1',
    'install_requires': ['smtplib', 'PyQuery', 'sqlite3'],
    'packages': ['jobBot'],
    'scripts': [],
    'name': 'jobBot'
}

setup(**config)