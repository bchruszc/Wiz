#!/bin/sh
django-admin.py dumpdata --pythonpath=/home/brad/html/nascar/2008 --settings=system.settings --format=xml --indent=2 pool