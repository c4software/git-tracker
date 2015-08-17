import subprocess
import json

from extended_BaseHTTPServer import serve,route
from jinja_helper import render

@route("/",["GET"])
def home(**kwargs):
    return render("liste.html")

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
