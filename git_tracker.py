import subprocess
import json

from extended_BaseHTTPServer import serve, route, override
from jinja_helper import render, get_wd

@route("/",["GET"])
def home(**kwargs):
    return render("liste.html")

@override("static")
def handler_static(o, arguments, action):
    try:
        return {"content": open(get_wd()+o.path).read().replace('\n',''), "header":{"Content-type":"text/css"}}
    except Exception as e:
        print e
        return "404"
# API
@route("/get_author",["GET"])
def get_author(**kwargs):
    command = "git log --all --format='%aN <%cE>' | sort -u"
    try:
        output = subprocess.check_output(command, shell=True).splitlines()
        return json.dumps(output)
    except:
        return json.dumps([])

if __name__ == '__main__':
    serve(ip="0.0.0.0", port=5000)
