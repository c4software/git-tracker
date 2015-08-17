import subprocess
import json
import mimetypes
import hashlib
import re

from os import listdir
from os.path import isfile, join


from extended_BaseHTTPServer import serve, route, override
from jinja_helper import render, get_wd
from tools import sorted_ls

issuer_folder = ".git_tracker"

@route("/",["GET"])
def home(**kwargs):
    # Get issue liste
    issue_list = []
    for f in sorted_ls(issuer_folder):
        try:
            issue = json.load(open(join(issuer_folder,f)))
            issue["id"] = f
            issue_list.append(issue)
        except Exception as e:
            print e
            pass

    return render("liste.html", {"issues": issue_list})

@route("/author",["GET"])
def author(**kwargs):
    author_list = []
    for author in json.loads(get_author()):
        try:
            m = re.search('(.+?) <(.+?)>', author)
            author_list.append({"name": m.group(1), "hash": hashlib.md5(m.group(2)).hexdigest()})
        except Exception as e:
            author_list.append({"name": author})

    return render("author.html", {"authors": author_list})


@override("static")
def handler_static(o, arguments, action):
    try:
        mimetype, encode = mimetypes.guess_type(get_wd()+o.path)
        return {"content": open(get_wd()+o.path).read(), "Content-type": mimetype}
    except Exception as e:
        return ""
        pass

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
