#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gunicorn -w 4 SpiderKeeper.uwsgi:app
"""

from SpiderKeeper.app import app, initialize

initialize()
