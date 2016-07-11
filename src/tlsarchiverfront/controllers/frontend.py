#!/usr/bin/env python

import datetime

from flask import Blueprint, request, render_template
from tlsarchiverfront import app
from tlsarchiverfront.services.stats import get_stats
from tlsarchiverfront.services.cryptostats import get_protocols_stats, get_ciphersuites_stats
from tlsarchiverfront.services.certslist import get_certificates_list, get_hosts_list


frontend = Blueprint('frontend', __name__)


@frontend.route('/certs')
def index():
    page = request.args.get('page', 0)

    try:
        page = int(page)
    except ValueError:
        page = 0

    return render_template(
        'certslist.html',
        config=app.config,
        certificates=get_certificates_list(page=page),
        page=page,
    )


@frontend.route('/')
def hosts():
    # TODO: use a decorator for pagination
    page = request.args.get('page', 0)

    try:
        page = int(page)
    except ValueError:
        page = 0

    return render_template(
        'hostslist.html',
        hosts=get_hosts_list(page=page),
        page=page,
    )


@frontend.route('/stats')
def stats():
    return render_template(
        'stats.html',
        config=app.config,
        stats=get_stats(),
    )


@frontend.route('/crypto')
def crypto():
    return render_template(
        'crypto.html',
        config=app.config,
        protocols=get_protocols_stats(),
        ciphersuites=get_ciphersuites_stats(),
    )
