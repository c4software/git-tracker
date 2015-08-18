import os
import subprocess
import unicodedata

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
