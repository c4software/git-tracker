import os
import glob
import subprocess
import unicodedata
import time
import datetime
import json
import base64
import re

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

def create_issue(issue_folder, author_name, author_email, data):
    # Issue are named with a filename starting by a i followed by the timestamp of
    # the creation.
    # Ex : i100000
    issue = {
        "author": "{0} <{1}>".format(author_name, author_email),
        "title": data.get('title', [""]).pop(),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "label": data.get('label', [""]).pop(),
        "state": "Open",
        "content": base64.b64encode(data.get('description', [""]).pop())
    }

    # Write to disk
    f = open("{0}/i{1}".format(issue_folder, time.time()),'w')
    f.write(json.dumps(issue))
    f.close()

def create_comment(issue_folder, author_name, author_email, data, related_issue):
    # Comment are named withe a filename starting by a r followed by the timestamp
    # of the related_issue and followed by the timestamp of the creation
    # Ex : r100000_1000001
    issue = {
        "author": "{0} <{1}>".format(author_name, author_email),
        "created_at": datetime.datetime.now().isoformat(),
        "content": base64.b64encode(data)
    }

    # Write to disk
    comment_id = "r{0}_{1}".format(related_issue, time.time())
    f = open("{0}/{1}".format(issue_folder, comment_id),'w')
    f.write(json.dumps(issue))
    f.close()

    return comment_id
