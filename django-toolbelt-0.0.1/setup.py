# -*- coding: utf-8 -*-
"""
Django-Toolbelt
~~~~~~~~~~~~~~~

This is a simple package that simply requires the following packages:

    - django
    - psycopg2
    - gunicorn
    - dj-database-url
    - dj-static

"""

from setuptools import setup

requires = [
    'django',
    'psycopg2',
    'gunicorn',
    'dj-database-url',
    'dj-static'
]

setup(
    name='django-toolbelt',
    version='0.0.1',
    url='https://devcenter.heroku.com/articles/django',
    # license='BSD',
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    description='A simple collection of common Django utilities.',
    long_description=__doc__,
    py_modules=[],
    zip_safe=False,
    install_requires=requires,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
