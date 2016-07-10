#!/usr/bin/env python

import os

FLASK_APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask
from flask import Flask
app = Flask(__name__)


# Config
if os.getenv('DEV') == 'yes':
    app.config.from_object('tlsarchiverfront.config.DevelopmentConfig')
    app.logger.info("Config: Development")
elif os.getenv('TEST') == 'yes':
    app.config.from_object('tlsarchiverfront.config.TestConfig')
    app.logger.info("Config: Test")
else:
    app.config.from_object('tlsarchiverfront.config.ProductionConfig')
    app.logger.info("Config: Production")

# Logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# Email on errors
if not app.debug and not app.testing:
    import logging.handlers
    mail_handler = logging.handlers.SMTPHandler(
        'localhost',
        os.getenv('USER'),
        app.config['SYS_ADMINS'],
        '{0} error'.format(app.config['SITE_NAME']),
    )
    mail_handler.setFormatter(logging.Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
    '''.strip()))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    app.logger.info("Emailing on error is ENABLED")
else:
    app.logger.info("Emailing on error is DISABLED")

#
# # Email
# from flask.ext.mail import Mail
# mail = Mail(app)

# Memcache
from werkzeug.contrib.cache import MemcachedCache
app.cache = MemcachedCache(app.config['MEMCACHED_SERVERS'])


def cache_fetch(key, value_function, timeout=None):
    '''Mimicking Rails.cache.fetch'''
    global app
    self = app.cache
    data = self.get(key)
    if data is None:
        data = value_function()
        self.set(key, data, timeout)
    return data
app.cache.fetch = cache_fetch


# Helpers
from tlsarchiverfront.helpers import datetimeformat
app.jinja_env.filters['datetimeformat'] = datetimeformat

# Business Logic
# http://flask.pocoo.org/docs/patterns/packages/
# http://flask.pocoo.org/docs/blueprints/
from tlsarchiverfront.controllers.frontend import frontend
app.register_blueprint(frontend)
