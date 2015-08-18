import os
import subprocess
import unicodedata
import time
import datetime
import json
import base64

def sorted_ls(path):
    try:
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))
    except:
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


def create_issue(issue_folder, author_name, author_email, data):
    issue = {
        "author": "{0} <{1}>".format(author_name, author_email),
        "title": data.get('title', [""]).pop(),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "label": data.get('label', [""]).pop(),
        "content": base64.b64encode(data.get('description', [""]).pop()),
        "comments": []
    }

    # Write to disk
    f = open("{0}/{1}".format(issue_folder, int(time.time())),'w')
    f.write(json.dumps(issue))
    f.close()
