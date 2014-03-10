import os
import re
import time
from PIL import Image
from PIL.ExifTags import TAGS
from lol import logger

__author__ = 'samip_000'

from PIL import Image
from PIL.ExifTags import TAGS

#import *
#from imagefuncs import ensure_dir, get_exif_data, get_dt, get_camera, get_uniqueid


def ensure_dir(f):
    #print "ensuring dir", f
    d = os.path.dirname(f)
    if not os.path.exists(f):
        os.makedirs(f)
        logger.info("Created dir %s",f)
        #print "created dir",f
    else:
        pass
        #print "not created, exists",f
    return d


def get_exif_data(fname):
    """Get embedded EXIF data from image file."""
    ret = {}
    exifinfo = None
    try:
        img = Image.open(fname)
        if hasattr(img, '_getexif'):
            try:
                exifinfo = img._getexif()
            except:
                exifinto = None
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    except IOError:
        logger.error("IOERROR %s" , fname)
    return ret


def get_dt(data, f, abspath):
    logger.debug(data)
    if 'DateTime' in data:
        ftime = data['DateTime']
    elif 'DateTimeOriginal' in data:
        ftime = data['DateTimeOriginal']
    else:
        ftime = ''
    try:
        ftime = ftime.replace(' ', '-')
        ftime = ftime.replace(':', '-')
        ftime = ftime.replace('\\', '-')
    except:
        ftime = ''

    if ftime != '':
        return ftime

        # capture time from filename : dd-mm-yyyy
    try:
            m = re.search('\b(\d{2}-\d{2}-\d{4})\.', f)
            if m.group(1):
                match = m.group(1)
                dd = match[:2]
                mm = match[4:5]
                yy = match[6:9]
                return yy + "-" + mm + "-" + dd + "_00-00-00"
    except:
            pass

    try:
            # capture time from filename : yyyy-mm-dd
            m = re.search('\b(\d{4}-\d{2}-\d{2})\.', f)
            if m.group(1):
                match = m.group(1)
                yy = match[:3]
                dd = match[8:9]
                mm = match[5:6]
                return yy + "-" + mm + "-" + dd + "_00-00-00"
    except:
            pass
    try:
            m = re.search('\b(\d{8})\.', f)
            if m.group(1):
                match = m.group(1)
                yy = match[:3]
                mm = match[4:5]
                dd = match[6:7]
                return yy + "-" + mm + "-" + dd + "_00-00-00"
    except:
            pass
    try:
      t = os.path.getmtime(abspath)
      ftime = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime(t))
      return ftime
    except:
      return "0000-00-0000-00-00"


def get_camera(data):
    try:

        ret = data['Model'].replace(' ', '_').replace('/', "_").strip() + "_" + data['Make'].replace(' ', '_').replace('/', "_").strip()

        return ret.replace(" ", "")

    except:
        try:
            return data['Make']
        except:
            return ''


def get_uniqueid(data):
    try:
        return data['ImageUniqueID']
    except:
        return ''