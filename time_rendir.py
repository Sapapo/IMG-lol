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




def rename_duplicates(dirc):
    f = None
    f1 = None

    logger.info ("Now processing directory: ---------: %s", dirc)
    seen = {}  # limit ren to each dir
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
                abspath = os.path.join(dirc, f1)

                data = get_exif_data(abspath)
                tstamp = get_dt(data, f, abspath)
                sha1 = sha1offile(abspath)

                if args.method == "both":
                    key = xstr(tstamp) + "-" + sha1
                elif args.method == "sha1":
                    key = sha1
                elif args.method == "time":
                    key = tstamp
                else:
                    key = str(counter)

                try:
                    asset = seen[key]
                    logger.debug("seen before")
                    #asset["counter"] = asset["counter"] +1
                    asset["occurences"] += 1
                except KeyError:
                    try:
                        # no function to process files with extension 'ext', ignore it
                        logger.debug("New item")
                        seen[key] = {"counter": counter, "occurences": 1}
                        counter += 1
                        asset = seen[key]
                        #logger.info("Seen so far: %s", len(seen))
                    except:
                        traceback.print_exc(file=sys.stdout)
                    pass

                if args.operation == "rename":
                    new_filename = xstr(asset["counter"]).zfill(6) + "-" + xstr(asset["occurences"]).zfill(
                        3) + "-" + xstr(f)
                    #print new_filename
                    logger.info("Renaming file %s into %s", abspath, new_filename)
                    if not args.simulate:
                        shutil.move(abspath, dirc + "/" + new_filename)
                    else:
                        logger.debug("noo.. just simulating")

                elif args.operation == "move":
                    if asset["occurences"] > 1:
                        logger.info("Moving file %s into %s", abspath, args.target + "/" + f)
                        ensure_dir(args.target)
                        if not args.simulate:
                            shutil.move(abspath, args.target + "/" + f)
                        else:
                            logger.info("noo.. just simulating")
                elif args.operation == "move1st":
                    if asset["occurences"] == 1:
                        logger.info("Moving file %s into %s", abspath, args.target + "/" + f)
                        ensure_dir(args.target)
                        if not args.simulate:
                            shutil.move(abspath, args.target + "/" + f)
                        else:
                            logger.debug("noo.. just simulating")
                elif args.operation == "delete":
                    if asset["occurences"] > 1:
                        logger.info("Removing %s", abspath)
                        if not args.simulate:
                            os.remove(abspath)
                            logger.info("%s  #deleted",abspath)
                        else:
                            logger.debug("noo.. just simulating")
                    #shutil.copyfile
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




