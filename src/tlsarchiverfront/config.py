#!/usr/bin/env python
import os

# http://flask.pocoo.org/docs/config/#development-production

__all__ = ['Config', 'ProductionConfig', 'TestConfig', 'DevelopmentConfig']

DB_CREDENTIALS = '{}:{}'.format(
    os.getenv('TLSA_DB_USER', 'archiver'),
    os.getenv('TLSA_DB_PASSWORD', ''),
)


class Config(object):
    SECRET_KEY = '{SECRET_KEY}'
    SITE_NAME = '{SITE_NAME}'
    MEMCACHED_SERVERS = ['localhost:11211']
    SYS_ADMINS = ['foo@example.com']
    DB_URL = 'postgres://{}@db:5432/archives'.format(DB_CREDENTIALS)


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    DEBUG = False
    TESTING = True


class DevelopmentConfig(Config):
    '''Use "if app.debug" anywhere in your code, that code will run in development code.'''
    DEBUG = True
    TESTING = True
    DB_URL = 'postgres://{}@localhost:5432/archives'.format(DB_CREDENTIALS)
