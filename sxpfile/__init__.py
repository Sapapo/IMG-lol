import hashlib
import os
import sys
import traceback

__author__ = 'samip_000'


def sha1offile(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha1(f.read()).hexdigest()
    except:
        return "00000000000000"

def filesize(p):
  try:
    return os.path.getsize(p)
  except:
    return -1

def reverse_dirpath(p, maxlen=32):
    try:
        path = os.path.normpath(p)
        #path.replace('\\',os.pathsep)
        #path.replace('/',os.pathsep)
        path = path.replace(':', '')
        path = path.replace(' ', '_')

        folders = []
        folders = path.split('\\')
        #print folders
        folders.reverse()
        #print folders

        ret = "-".join(folders)
        return ret.replace('\\', '_').replace(':', '')[:maxlen]
    except:
        traceback.print_exc(file=sys.stdout)
        print "OOPS!"
        return p.replace(os.sep, "-").replace(' ', '_')[:maxlen]