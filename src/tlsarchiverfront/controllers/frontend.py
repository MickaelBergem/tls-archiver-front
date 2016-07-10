#!/usr/bin/env python

import datetime

from flask import Blueprint, request, render_template
from tlsarchiverfront import app
from tlsarchiverfront.services.stats import get_stats
from tlsarchiverfront.services.certslist import get_certificates_list


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
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
                page=page
            )


@frontend.route('/stats')
def stats():
    return render_template(
                'stats.html',
                config=app.config,
                stats=get_stats(),
            )
