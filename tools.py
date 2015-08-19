import os
import glob
import subprocess
import unicodedata
import time
import datetime
import json
import base64
import re

import settings

def sorted_ls(path):
    try:
        files = glob.glob(path)
        files.sort(key=os.path.getmtime)
        return files
    except Exception as e:
        print(e)
        return []

def exec_command(command):
    try:
        output = subprocess.check_output(command, shell=True)# .encode('unicode-escape').splitlines()
        output = unicode(output,'utf-8')
        output = unicodedata.normalize('NFD', output).encode('ascii', 'ignore')
        return output.splitlines()
    except Exception as e:
        print e
        return []

def extract_email_author(author):
    m = re.search('(.+?) <(.+?)>', author)
    return (m.group(1), m.group(2))

def create_issue(issue_folder, data):
    # Issue are named with a filename starting by a i followed by the timestamp of
    # the creation.
    # Ex : i100000
    issue = {
        "author": "{0} <{1}>".format(settings.author_name, settings.author_email),
        "title": data.get('title', [""]).pop(),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "label": data.get('label', [""]).pop(),
        "state": "Open",
        "assign_to": data.get('assignto', [""]).pop(),
        "content": base64.b64encode(data.get('description', [""]).pop())
    }

    # Write to disk
    f = open("{0}/i{1}".format(issue_folder, time.time()),'w')
    f.write(json.dumps(issue))
    f.close()

def create_comment(issue_folder, data, related_issue):
    # Comment are named withe a filename starting by a r followed by the timestamp
    # of the related_issue and followed by the timestamp of the creation
    # Ex : r100000_1000001
    issue = {
        "author": "{0} <{1}>".format(settings.author_name, settings.author_email),
        "created_at": datetime.datetime.now().isoformat(),
        "content": base64.b64encode(data)
    }

    # Write to disk
    comment_id = "r{0}_{1}".format(related_issue, time.time())
    f = open("{0}/{1}".format(issue_folder, comment_id),'w')
    f.write(json.dumps(issue))
    f.close()

    return comment_id

def load_issue(issue_folder, issue_id):
    try:
        f = open("{0}/{1}".format(issue_folder, issue_id),'r')
        return json.load(f)
    except Exception as e:
        pass
    finally:
        if f:
            f.close()

def write_issue(issue_folder, issue_id, issue):
    try:
        f = open("{0}/{1}".format(issue_folder, issue_id),'w')
        f.write(json.dumps(issue))
    except Exception as e:
        pass
    finally:
        if f:
            f.close()

def update_assign(issue_folder, issue_id, assignto):
    issue = load_issue(issue_folder, issue_id)
    issue['assign_to'] = assignto
    write_issue(issue_folder, issue_id, issue)
    if assignto == "":
        create_comment(issue_folder, "*Assignee removed*", issue_id)
    else:
        create_comment(issue_folder, "*Reassigned to '{0}'*".format(assignto), issue_id)

def change_state(issue_folder, issue_id, state):
    issue = load_issue(issue_folder, issue_id)
    issue['state'] = state
    write_issue(issue_folder, issue_id, issue)
    create_comment(issue_folder, "*Status changed to {0}*".format(state), issue_id)
