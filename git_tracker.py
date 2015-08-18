# -*- coding: utf-8 -*-

import json
import mimetypes
import hashlib
import re

import os
from os import listdir
from os.path import isfile, join


from extended_BaseHTTPServer import serve, route, override, redirect
from jinja_helper import render, get_wd
from tools import sorted_ls, exec_command

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

@route("/issue",["GET"])
def issue(**kwargs):
    if "id" not in kwargs:
        return redirect("/")

    # Load de l'issue
    try:
        id_issue = kwargs.get("id")[0]
        issue = json.load(open(join(issuer_folder,id_issue)))
    except:
        return redirect("/")

    return render("issue.html", {"issue": issue})

@route("/create", ['GET'])
def create(**kwargs):
    return render("create.html", {"author": get_author()})

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

@route("/branch", ["GET"])
def branch():
    return render("branch.html", {"branchs": json.loads(get_branch())})

@route("/log", ["GET"])
def branch():
    return render("log.html", {"logs": json.loads(get_log())})


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
    return json.dumps(exec_command("git log --all --format='%aN <%cE>' | sort -u"))

@route("/get_branch",["GET"])
def get_branch(**kwargs):
    return json.dumps(exec_command("git branch -a"))

@route("/get_log",["GET"])
def get_log(**kwargs):
    return json.dumps(exec_command("git log --pretty=format:'%h - %an, %ar : %s' -50"))

author_email = "anon@anon.com"
author_name = "Anonymous"

if __name__ == '__main__':
    # Init folder for issue
    if not os.path.exists(issuer_folder):
        os.makedirs(issuer_folder)

    # Get user configuration for issue creation
    try:
        author_email = exec_command("git config user.name").pop()
    except:
        print ("Username unavailable. You are now : {0}".format(author_name))

    try:
        author_email = exec_command("git config user.email").pop()
    except:
        print ("Email unavailable. You are now : {0}".format(author_email))


    serve(ip="0.0.0.0", port=5000)
