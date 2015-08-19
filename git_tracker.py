# -*- coding: utf-8 -*-

import json
import mimetypes
import hashlib
import re

import os
from os import listdir
from os.path import isfile, join

import settings
from extended_BaseHTTPServer import serve, route, override, redirect
from jinja_helper import render, get_wd
from markdown_helper import decode_markdown
from tools import sorted_ls, exec_command, create_issue, create_comment, extract_email_author, update_assign, change_state

issue_folder = ".git_tracker"

@route("/",["GET"])
def home(**kwargs):
    # Get issue liste
    issue_list = []
    for f in sorted_ls("{0}/i*".format(issue_folder)):
        try:
            issue = json.load(open(f))
            issue["id"] = os.path.basename(f)
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
        issue = json.load(open(join(issue_folder,id_issue)))
    except:
        return redirect("/")

    # Decode description
    issue['id']         = id_issue
    issue['content']    = decode_markdown(issue.get("content", ""))

    issue["comments"]   = []
    # Get related comments
    for f in sorted_ls("{0}/r{1}_*".format(issue_folder, id_issue)):
        data = json.load(open(f))
        data["id"]      = os.path.basename(f)
        data["content"] = decode_markdown(data.get("content", ""))
        name, email     = extract_email_author(data.get("author", "Anon <anon@anon.com>"))
        data["hash"]    = hashlib.md5(email).hexdigest()
        issue["comments"].append(data)

    return render("issue.html", {"issue": issue, "authors": json.loads(get_author())})

@route("/change_assign_to", ['POST'])
def change_assign_to(**kwargs):
    issue_id = kwargs.get("issue_id",[""]).pop()
    assignto = kwargs.get("assignto",[""]).pop()
    update_assign(issue_folder, issue_id, assignto)
    return ""

@route("/add_comment", ['POST'])
def add_comment(**kwargs):
    related_issue = kwargs.get("issue_related_id",[""]).pop()
    newstate = kwargs.get("newstate",[None]).pop()

    if related_issue != "":
        comment_id = create_comment(issue_folder, kwargs.get("comments",[""]).pop(), related_issue)

    if newstate:
        comment_id = change_state(issue_folder, related_issue, newstate)

    return redirect("/issue?id={0}#{1}".format(related_issue, comment_id))

@route("/create", ['GET'])
def create(**kwargs):
    return render("create.html", {"authors": json.loads(get_author())})

@route("/create", ['POST'])
def handle_create(**kwargs):
    create_issue(issue_folder, kwargs)
    return redirect("/")

@route("/author",["GET"])
def author(**kwargs):
    author_list = []
    for author in json.loads(get_author()):
        try:
            name, email = extract_email_author(author)
            author_list.append({"name": name, "hash": hashlib.md5(email).hexdigest()})
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

if __name__ == '__main__':
    # Init folder for issue
    if not os.path.exists(issue_folder):
        os.makedirs(issue_folder)

    # Get user configuration for issue creation
    try:
        settings.author_name = exec_command("git config user.name").pop()
    except:
        print ("Username unavailable. You are now : {0}".format(settings.author_name))

    try:
        settings.author_email = exec_command("git config user.email").pop()
    except:
        print ("Email unavailable. You are now : {0}".format(settings.author_email))

    print ("Git-Tracker is now listening on http://localhost:5000/ ")
    serve(ip="localhost", port=5000)
