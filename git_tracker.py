# -*- coding: utf-8 -*-

import json
import mimetypes
import hashlib
import re
import time
import os
from os import listdir
from os.path import isfile, join
import base64

import settings
from extended_BaseHTTPServer import serve, route, override, redirect
from jinja_helper import render, get_wd
from markdown_helper import decode_markdown
from tools import sorted_ls, exec_command, create_issue, load_issue, create_comment, extract_email_author, update_assign, change_state, update_issue

issue_folder = ".git_tracker"

@route("/",["GET"])
def home(**kwargs):
    # Get issue liste
    issue_list = []
    for f in sorted_ls("{0}/i*".format(issue_folder)):
        try:
            issue = load_issue(issue_folder,  os.path.basename(f))
            issue["id"] = os.path.basename(f)
            issue_list.append(issue)
        except Exception as e:
            print (e)
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

@route("/update", ['GET'])
def update(**kwargs):
    try:
        id_issue = kwargs.get("id")[0]
        issue = json.load(open(join(issue_folder,id_issue)))
        issue["content"] = base64.b64decode(issue["content"])
        return render("update.html", {"issue": issue, "issue_id": id_issue})
    except:
        return redirect("/")

@route("/update", ['POST'])
def handle_update(**kwargs):
    if "issue_id" in kwargs:
        try:
            update_issue(issue_folder, kwargs)
            return redirect("/issue?id={0}".format(kwargs.get("issue_id")[0]))
        except Exception as e:
            print (e)
    else:
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

@route("/stats", ["GET"])
def branch():
    return render("stats.html", {"stats": json.loads(get_stats()), "nb_commits": json.loads(get_number_of_commits())})


@route("/log", ["GET"])
def branch():
    logs = json.loads(get_log())
    formated_logs = []
    for log in logs:
        log = log.split(";")
        formated_logs.append({
        "commit_hash": log.pop(0),
        "username":log.pop(0),
        "hash":hashlib.md5(log.pop(0)).hexdigest(),
        "date":log.pop(0),
        "message":" ".join(log[:])
        })

    return render("log.html", {"logs": formated_logs})


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
    return json.dumps(exec_command("git log --pretty=format:'%h;%an;%ae;%ar;%s' -50"))

@route("/get_number_of_commits", ["GET"])
def get_number_of_commits(**kwargs):
    try:
        return json.dumps(exec_command("git rev-list HEAD --count"))
    except Exception as e:
        return [""]

@route("/get_stats",["GET"])
def get_stats(**kwargs):
    try:
        oldest_commit       = exec_command("git log --pretty=oneline --reverse --format='%ct' | head -1")
        days_project        = int(time.time()-float(oldest_commit.pop(0)))/60/60/24;
        stats               = exec_command("git shortlog -s -n --all")
        result              = []
        for x in stats:
            x = x.lstrip().split("\t")
            x.append("{0:.2f}".format(float(x[0])/days_project))
            result.append(x)

        return json.dumps(result)
    except Exception as e:
        print(e)
        return [""]

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
