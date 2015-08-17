import os
from jinja2 import Environment, FileSystemLoader

def render(tpl, fields={}):
    try:
        path = "{0}/templates/".format(get_wd())
        content = open("{0}{1}".format(path, tpl)).read().replace('\n','')
        env = Environment(loader=FileSystemLoader(path))
        tpl = env.from_string(content)
        return tpl.render(**dict(fields.items()))
    except Exception as e:
        return ""

def get_wd():
    return os.path.dirname(os.path.realpath(__file__))
