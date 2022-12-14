#!/usr/bin/env python3
# Quick and dirty buscacursos/catalogo scraper based on the scraper for ramos-uc

import os
import traceback
from bc_scraper.actions.collect import CollectCourses
import json
import logging
import sys

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

cookies = ""
if os.path.exists(".cred"):
    try:
        with open(".cred", 'r') as file:
            cookies = file.read()
        log.info(f"using cookies = '{cookies}'")
    except Exception:
        log.error("reading .cred for cookies failed:")
        log.error(traceback.format_exc())


args = sys.argv.copy()
args.pop(0)
opts = set()
for i in reversed(range(len(args))):
    if args[i].startswith("--"):
        opts.add(args[i][2:])
        args.pop(i)

if len(args) == 0:
    print("usage: python3 main.py [--test] [periods...]")
    print("  example: python3 main.py 2022-2 2022-1 > data.json 2> log.txt")
    sys.exit()
periods = args

settings = {"batch_size": 100, "cookies": cookies, "testmode": "test" in opts}

data = {}
for period in periods:
    courses = CollectCourses()
    courses.collect(period, settings)
    for course in courses.courses.values():
        course['sections'] = dict(
            sorted(course["sections"].items(), key=lambda x: int(x[0])))
    data[period] = dict(sorted(courses.courses.items()))
data = dict(sorted(data.items(), reverse=True))
json.dump(data, sys.stdout)
