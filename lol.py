from imagefuncs import *
from sxpfile import *
from sxpstring import *

__author__ = 'samip_000'

import argparse
import logging
import os
import shutil
import traceback
import sys

from PIL import Image


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

prev_y = "0000"
prev_m = "00"


"""parser.add_argument('--foo', action='store_true')

"""

seen = {}



def get_seen_set(dirc):
    global seen
    try:
        for f in os.listdir(dirc):
            try:
                f1 = dirc.decode('utf-8', 'ignore') + '/' + f.decode('utf-8', 'ignore')
            except:
                pass
            if os.path.isdir(f1):
                get_seen_set(f1)
                continue
            else:
                logger.info("processing %s",f)
                abspath = os.path.join(dirc, f)

                sha1 = sha1offile(abspath)
                sz = filesize(abspath)
                key = xstr(sz) + "-" + xstr(sha1)
                seen [key] = abspath
    except:
        traceback.print_exc(file=sys.stdout)
        pass






def getseenchecksums(path):
    """


    """
    return






prev_dir = None


def copy(sourced, filename, dest):
    try:
        d = os.path.join(dest, filename)
        #shutil.copyfile (f, d)

        shutil.copyfile(sourced+"/"+filename,dest+"/"+filename)
        #prev_dir = dest
    except:
        return








def exif_copy_cr2(dirpath, f, root):
    global prev_y, prev_m

    logger.info("processing file %s (%s)",f,dirpath)
    fn = None
    abspath_jpg = os.path.join(dirpath, os.path.splitext(f)[0] + ".jpg")
    abspath_cr2 = os.path.join(dirpath, f)
    sha1 = sha1offile(abspath_cr2)
    data = get_exif_data(abspath_jpg)
    tstamp = get_dt(data, f, abspath_jpg)

    postpostfix = ''
    preprefix = ''
    sizestr = ''
    try:
        year = tstamp[:4]
        mon = tstamp[5:7]
        if(int(year)<1981):
            year = prev_y
            mon = prev_m

    except:
        year = prev_y
        mon = prev_m


    if year is None:
        year = "NaN"
    if mon is None:
        year = "NaN"

    year = force_numeric(year,"1943",4)
    mon = force_numeric(mon,"00",2)

    try:
        img = Image.open(abspath_jpg)
        width, height = img.size
        sizestr = str(width) + "x" + str(height)
        if width < 200 and height < 200:
            preprefix = "tn_"
            return
    except:
        postpostfix = ""
        width = ''
        height = ''
        sizestr = ''
    ensure_dir(args.target)
    yd = os.path.join(args.target, year)
    #print yd
    #print yd
    yd2 = ensure_dir(yd)
    md = os.path.join(yd, mon)
    kk = ensure_dir(md.decode('utf-8', 'ignore'))
    #print md

    camera = a_(get_camera(data),32).strip()
    uniqueid = a_(get_uniqueid(data),16)
    dp = a_(reverse_dirpath(dirpath, 48).replace(':', "W").replace('/', "Q"), 48)
    if dp == ".":
            dp = ''


    ensure_dir(args.target + "/" + year + "/" + mon)
    #dest_dir= "i:/IM/"+year+"/"+mon
    try:
        fn = args.target + "/" + year + "/" + mon + "/" + \
            appif('', xstr(preprefix), '') + \
            appif('', xstr(tstamp), "_") + \
            appif('{', xstr(args.prefix), '}_') + \
            appif('[', a_(u_(xstr(os.path.splitext(f)[0])),48),"]") + \
            appif("(",sizestr, ")") + \
            appif('-[', a_(u_(xstr(camera).decode('utf-8', 'ignore')),32), "]") + \
            appif("-[UI-", xstr(uniqueid), "]") + \
            appif("-[", xstr(sha1), "]") + xstr(args.postfix) + xstr(postpostfix) + \
            appif('-[', dp,']') + \
            xstr(os.path.splitext(f)[1])
    except:
        traceback.print_exc(file=sys.stdout)
    de = os.path.join(md, fn.decode('utf-8', 'ignore'))
    print "source ", abspath_cr2.decode('utf-8', 'ignore'), "target ", de.decode('utf-8', 'ignore')
    #ddd = dest.decode('utf-8','ignore')
    if os.path.isfile(de):
        logger.info("File exists %s", de)
    else:
        try:
            shutil.copyfile(abspath_cr2, fn)
            logger.info("copied file to %s",fn)
            prev_y = year
            prev_m = mon

        except:
            traceback.print_exc(file=sys.stdout)
            try:
                shutil.copyfile(abspath_cr2.decode('utf-8', 'ignore'), fn)
                prev_y = year
                prev_m = mon

            except:
                traceback.print_exc(file=sys.stdout)
                shutil.copyfile(abspath_cr2.decode('utf-8', 'ignore'), args.target + "/" + year + "/" + mon + "/" + f)
                prev_y = year
                prev_m = mon

                pass

    #print "Copied"
    try:
        sha1_p = sha1offile(fn)
    except:
        sha1_p = ''
    if sha1 == sha1_p:
        pass
        #print "SHA1 OK"
    else:
        print "SHA1 NOK"

    return




def writeDict(dict, filename, sep):
  try:
    with open(filename, "a") as f:
        for i in dict.keys():
            f.write(i + " " + sep.join([str(x) for x in dict[i]]) + "\n")
  except:
    return

def readDict(filename, sep):
  try:
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            values = line.split(sep)
            dict[values[0]] = {int(x) for x in values[1:len(values)]}
        return(dict)
  except:
      return {}
# and later:
   # filtered_data = filter(filter_func, data).lower()

def cc_ (s):
    if s is not None and s.endswith("."):
        s= s.replace(".","")
    return s


def exif_copy(dirpath, f, root):
    global prev_y, prev_m
    logger.info("processing file %s (%s)",f,dirpath)
    abspath = os.path.join(dirpath, f)
    sha1 = sha1offile(abspath)
    sz = filesize (abspath)
    key = xstr(sz) + "-" + xstr(sha1)
    try:
      copy_of = seen[key]
      logger.info("%s is copy of %s", abspath,copy_of)
      return
    except KeyError:
      seen[key] = abspath

    data = get_exif_data(abspath)
    tstamp = get_dt(data, f, abspath)
    de = None
    fn = None

    postpostfix = ''
    preprefix = ''
    sizestr = ''
    try:
        year = tstamp[:4]
        mon = tstamp[5:7]
        if(int(year)<1981):
            year = prev_y
            mon = prev_m

    except:
        year = prev_y
        mon = prev_m
        tstamp = ''





    if year is None:
        year = "NaN"
    if mon is None:
        year = "00"

    year = force_numeric(year,"1943",4)
    mon = force_numeric(mon,"00",2)


    try:
        img = Image.open(abspath)
        width, height = img.size
        sizestr = str(width) + "x" + str(height)
        if width < 200 and height < 200:
            if (args.skipthumb):
                return
            preprefix = "tn_"
    except:
        postpostfix = "_(rikki)"
        if (args.skipbroken):
            return
        width = ''
        height = ''
        sizestr = ''


    ensure_dir(args.target)
    yd = os.path.join(args.target, year)
    yd2 = ensure_dir(yd)
    md = os.path.join(yd, mon)
    kk = ensure_dir(md.decode('utf-8', 'ignore'))

    camera = a_(u_(get_camera(data)),32).strip()
    uniqueid = get_uniqueid(data)
    #print "pre",tstamp

    tstamp = filter(filter_func, tstamp)
    #print "post",tstamp

    camera = filter(filter_func, camera)
    #print "[["+camera+"]]"

    try:

        #* force year if needed */
        if args.year:
            year = args.year

        if args.skipdir:
            dirpath = ''

        try:
            ensure_dir(args.target + "/" + year + "/" + mon)
            de = md
        except:

            de = args.target + "/" + "talle"
            ensure_dir(de)
        dp = a_(reverse_dirpath(dirpath, 48).replace(':', "W").replace('/', "Q"), 48)
        if dp == ".":
            dp = ''


        #dest_dir= "i:/IM/"+year+"/"+mon
        try:
            if args.original:
              fn = args.target + "/" + year + "/" + mon + "/" + f
            else:
              fn = args.target + "/" + year + "/" + mon + "/" + \
                appif('', xstr(preprefix), '') + \
                appif('', xstr(tstamp), "_") + \
                appif('{', xstr(args.prefix), '}_') + \
                appif('[', cc_(a_(u_(xstr(os.path.splitext(f)[0])),48)),"]") + \
                appif("(",xstr(sizestr), ")") + \
                appif('-[', a_(u_(xstr(camera).decode('utf-8', 'ignore')),32), "]") + \
                appif("-[UI-", xstr(uniqueid), "]") + \
                appif("-[", xstr(sha1), "]") + xstr(args.postfix) + xstr(postpostfix) + \
                appif('-[',dp ,']') + \
                xstr(os.path.splitext(f)[1])
        except:
            traceback.print_exc(file=sys.stdout)
        try:
            de = xstr(fn)
        except:
            pass
    except:
        traceback.print_exc(file=sys.stdout)
        pass
    try:
        if os.path.isfile(xstr(fn)):
            logger.info("Skipping. File exists %s", fn)
        else:
            try:
                if args.removeoriginal:
                    shutil.move(abspath, fn)
                else:
                    shutil.copyfile(abspath, fn)
                logger.info("copied(1) file to %s",fn)
                prev_y = year
                prev_m = mon

            except:
                logger.info("tried %s ->> %s",abspath, fn)

                traceback.print_exc(file=sys.stdout)
                try:
                    if args.removeoriginal:
                        shutil.move(abspath.decode('utf-8', 'ignore'), fn)
                    else:
                        shutil.copyfile(abspath.decode('utf-8', 'ignore'), fn)
                    prev_y = year
                    prev_m = mon
                    logger.info("copied(2) file to %s",fn)

                except:
                    logger.info("tried %s ->> %s",abspath.decode('utf-8', 'ignore'), fn)
                    traceback.print_exc(file=sys.stdout)
                    try:
                        if args.removeoriginal:
                            shutil.move(abspath.decode('utf-8', 'ignore'), args.target + "/" + year + "/" + mon + "/" + f)
                        else:
                            shutil.copyfile(abspath.decode('utf-8', 'ignore'), args.target + "/" + year + "/" + mon + "/" + f)
                        prev_y = year
                        prev_m = mon
                        fn = args.target + "/" + year + "/" + mon + "/" + f
                        logger.info("copied(3) file to %s",args.target + "/" + year + "/" + mon + "/" + f)
                    except:
                        traceback.print_exc(file=sys.stdout)
                        pass
    except:
            try:
                if args.removeoriginal:
                    shutil.move(abspath, fn)
                else:
                    shutil.copyfile(abspath, fn)
                logger.info("copied(1) file to %s",fn)
                prev_y = year
                prev_m = mon

            except:
                logger.info("tried %s ->> %s",abspath, fn)

                traceback.print_exc(file=sys.stdout)
                try:
                    if args.removeoriginal:
                        shutil.move(abspath.decode('utf-8', 'ignore'), fn)
                    else:
                        shutil.copyfile(abspath.decode('utf-8', 'ignore'), fn)
                    prev_y = year
                    prev_m = mon
                    logger.info("copied(2) file to %s",fn)

                except:
                    logger.info("tried %s ->> %s",abspath.decode('utf-8', 'ignore'), fn)
                    traceback.print_exc(file=sys.stdout)
                    try:
                        if args.removeoriginal:
                            shutil.move(abspath.decode('utf-8', 'ignore'), args.target + "/" + year + "/" + mon + "/" + f)
                        else:
                            shutil.copyfile(abspath.decode('utf-8', 'ignore'), args.target + "/" + year + "/" + mon + "/" + f)
                        prev_y = year
                        prev_m = mon
                        fn = args.target + "/" + year + "/" + mon + "/" + f
                        logger.info("copied(3) file to %s",args.target + "/" + year + "/" + mon + "/" + f)
                    except:
                        traceback.print_exc(file=sys.stdout)
                        pass


    try:
        sha1_p = sha1offile(fn)
    except:
        sha1_p = ''
    if sha1 == sha1_p:
        pass
    else:
        logger.warn("File; %s",fn)
        logger.warn("Sha1 warning: %s != %s",sha1,sha1_p)


    return


funcMap = {'.nef': exif_copy,'.gif': exif_copy, '.bmp': exif_copy,'.pdf': exif_copy, '.lrprev': copy, '.tif': exif_copy, '.png': exif_copy,  '.mpo': exif_copy , '.x': copy, '.jpg': exif_copy, '.avi': exif_copy, '.thm': exif_copy, '.cr2': exif_copy_cr2}


def process_images(path):
    #seen = getseenchecksums(args.target)
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            #for d in dirnames:
            #     print ">>",d
            for f in filenames:
                logger.info("%48s %s",f,dirpath)
                ext = os.path.splitext(f)[1]
                try:
                    function = funcMap[ext.lower()]
                except KeyError:
                    # no function to process files with extension 'ext', ignore it
                    if args.copyunknow>0:
                        shutil.copyfile(dirpath+"/"+f, args.target + "/" + prev_m + "/" + prev_y + "/" + f)
                    pass
                else:
                    #print dirpath, f
                    abspath = os.path.join(dirpath, f)
                    function(dirpath, f, args.target)

                if args.forcedelete:
                         logger.info("Deleting %s", f)
                         try:
                            os.remove(dirpath+"/"+f)
                         except:
                            pass
    except:
        traceback.print_exc(file=sys.stdout)


class VAction(argparse.Action):
    def __call__(self, vaparser, vargs, values, option_string=None):
        # print 'values: {v!r}'.format(v=values)
        if values is None:
            values = '1'
        try:
            values = int(values)
        except ValueError:
            values = values.count('v') + 1
        setattr(vargs, self.dest, values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IMG_LOL')
    parser.add_argument('-v', '--verbose', nargs='?', action=VAction, dest='verbose',
                        help='Verbose [Level]')
    parser.add_argument('-2', '--target', dest='target', default='d:/dest',
                        help='Target directory')
    parser.add_argument('-1', '--source', dest='source', default='d:\\_kuvia\\',
                        help='Source Directory')

    parser.add_argument('-3', '--appendix', dest='postfix',
                        help='Filename appendix')
    parser.add_argument('-4', '--prefix', dest='prefix',
                        help='Filename prefix')

    parser.add_argument('-5', '--year', dest='year',
                        help='Force year')

    parser.add_argument('-6', '--skipdir', dest='skipdir',
                        help='Leave dir out of filename')
    parser.add_argument('-t', '--skipthumb', dest='skipthumb',
                        help='Leave dir out of filename')
    parser.add_argument('-b', '--skipbroken', dest='skipbroken',
                        help='Leave dir out of filename')

    parser.add_argument('-7', '--skipseen', dest='skipseen',
                        help='Leave dir out of filename')

    parser.add_argument('-F', '--forcedelete', dest='forcedelete',
                        help='Delete processed files')

    parser.add_argument('-U', '--copyunknow', dest='copyunknow',
                        help='Delete processed files')

    parser.add_argument('-D', '--dict', dest='dict',
                        help='Delete processed files')
    parser.add_argument('-0', '--original', nargs='?',   dest='original',
                        help='Use Uriginal filename')

    parser.add_argument('-R', '--removeoriginal', dest='removeoriginal',
                        help='Delete processed files')

    parser.add_argument('-l', '--log', dest='logfile', help='logfile')
    #    parser.add_argument('-r', '--oper', dest='oper',default="policy"
    #                      ,help = 'Operation to perform:policy,tag')

    args = parser.parse_args()
    logging.info("Parsing arguments: Done.")

    #logger.setLevel(logging.WARNING)

    if args.dict:
       try:
         seen = readDict(args.dict, "|")
       except:
         pass

    if args.skipseen:
        pass
    else:
        get_seen_set(args.target)
        writeDict(seen, args.dict, "|")

    logging.info("Processing source dir of %s", args.source)

    process_images(args.source)

    if args.dict:
       writeDict(seen, args.dict, "|")

