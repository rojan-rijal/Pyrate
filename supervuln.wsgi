#!/usr/bin/python
import sys, os
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/supervuln/")
from app import create_app
application = create_app()
application.secret_key = 'supervuln_secret_key'
