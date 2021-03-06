# -*- coding: utf-8 -*-

import os
try:
    from jinja2 import Environment, FileSystemLoader
except:
    print("jinja2 is required")
    exit(255)

def render(tpl, fields={}):
    try:
        path = "{0}/templates/".format(get_wd())
        content = open("{0}{1}".format(path, tpl)).read()
        env = Environment(loader=FileSystemLoader(path))
        tpl = env.from_string(content)
        return tpl.render(fields)
    except Exception as e:
        print e
        return ""

def get_wd():
    return os.path.dirname(os.path.realpath(__file__))
