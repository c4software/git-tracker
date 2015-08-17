import os

def sorted_ls(path):
    try:
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))
    except:
        return []
