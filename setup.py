#!/usr/bin/env python

from distutils.core import setup

setup(
    name='django_rest_hipchat',
    version='0.0.1',
    description=(
        "Django Rest Framework based HipChat integration implementation."
    ),
    author="Nick Garanko",
    author_email='nick@itdude.eu',
    url='https://github.com/the-it-dude/django_rest_hipchat',
    packages=[
        'django_rest_hipchat',
        'django_rest_hipchat.migrations',
        'django_rest_hipchat.templates',
        'django_rest_hipchat.templates.django_rest_hipchat',
    ],
)
