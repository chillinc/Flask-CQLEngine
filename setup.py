#!/usr/bin/env python

import os
import re

from setuptools import setup


DIRNAME = os.path.abspath(os.path.dirname(__file__))
rel = lambda *parts: os.path.abspath(os.path.join(DIRNAME, *parts))

README = open(rel('README.md')).read()
INIT_PY = open(rel('flask_cqlengine.py')).read()
VERSION = re.findall("__version__ = '([^']+)'", INIT_PY)[0]


setup(
    name='flask-cqlengine',
    version=VERSION,
    description='Flask with cqlengine.',
    long_description=README,
    author='Michael Cyrulnik',
    author_email='michael@chill.com',
    url='https://github.com/chilldotcome/Flask-CQLEngine',
    dependency_links=[
        'git+git://github.com/chilldotcom/CQLEngine-Session#egg=CQLEngine-Session-0.1'
    ],
    install_requires=[
        'CQLEngine-Session>=0.1',
        'Flask',
        'cqlengine>=0.18'
    ],
    py_modules=[
        'flask_cqlengine',
    ],
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='flask cqlengine',
    license='BSD License',
)
