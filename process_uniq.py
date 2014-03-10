__author__ = 'samip_000'

import sys
import hashlib
import traceback
import shutil
import os
import argparse
import logging
import time


from sxpfile import sha1offile, reverse_dirpath
from sxpstring import xstr, appif, u_, a_, force_numeric, filter_func


from imagefuncs import *
from sxpfile import *
from sxpstring import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                seen [sha1] = abspath
    except:
        traceback.print_exc(file=sys.stdout)
        pass



def rename_duplicates(dirc):
    global seen

    f = None
    f1 = None

    logger.info ("Now processing directory: ---------: %s", dirc)
    counter = 1

    try:

        for f in os.listdir(dirc):

            try:
                f1 = dirc.decode('utf-8', 'ignore') + '/' + f.decode('utf-8', 'ignore')
            except:
                pass
            if os.path.isdir(f1):
                rename_duplicates(f1)
                continue
            else:
                logger.info("processing %s",f)
                abspath = os.path.join(dirc, f)

                sha1 = sha1offile(abspath)

                try:
                    copy_of  = seen[sha1]
                    logger.debug("seen before")
                    try:
                        if args.operation == "delete":
                            os.remove(abspath)
                            logger.info("%s. Removed ok as copy of %s",abspath,copy_of)
                        elif args.operation == "rename":
                            abspath2 = os.path.join(dirc, args.prefix + f)
                            shutil.move(abspath, abspath2)
                            logger.info("%s  Renamed to new name. %s",abspath2,copy_of)
                        elif args.operation == "move":
                            abspath2 = os.path.join(args.target , f)
                            shutil.move(abspath, abspath2)
                            logger.info("%s moved to %s. [%s",abspath,abspath2,copy_of)
                    except:
                        traceback.print_exc(file=sys.stdout)


                except KeyError:
                    pass
                    #
                    #try:


                        #logger.info("Seen so far: %s", len(seen))
                    #except:
                    #    traceback.print_exc(file=sys.stdout)
                    #pass

    except:
        traceback.print_exc(file=sys.stdout)
        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='IMG_LOL')
    parser.add_argument('-2', '--target', dest='target', default='d:/dest',
                        help='Target directory')
    parser.add_argument('-1', '--source', dest='source', default='d:\\_kuvia\\',
                        help='Source Directory')

    parser.add_argument('-3', '--method', dest='method',
                        help='time, sha1, both')
    parser.add_argument('-4', '--operation', dest='operation',
                        help='Operation: rename, delete, move')

    parser.add_argument('-5', '--simulate', dest='simulate',
                        help='Operation: rename, delete, move')

    parser.add_argument('-l', '--log', dest='logfile', help='logfile')
    #    parser.add_argument('-r', '--oper', dest='oper',default="policy"
    #                      ,help = 'Operation to perform:policy,tag')

    args = parser.parse_args()
    logging.info("Parsing arguments: Done.")

    #logger.setLevel(logging.WARNING)

    logging.info("Processing source dir of %s", args.source)
    cnt = 1
    if len(sys.argv) > 1:
        rename_duplicates(args.source)
    else:
        print "usage: rename_duplicates.py directory_of_photos_to_rename_by_timestamp"




