#!/usr/bin/python

import exifread
from datetime import datetime
import os
import sys

IMG_DATETIME_KEY = 'Image DateTime'

def validate(src_file):
  if not os.path.isfile(src_file):
    raise Exception("%s not exists." % src_file)
  if os.path.islink(src_file):
    raise Exception("%s is a symlink." % src_file)
  return True

def getIMGFilename(src_file):
  f = open(src_file, 'rb')
  tags = exifread.process_file(f, details=False, stop_tag="Image DateTime")
  img_filename = '';
  if IMG_DATETIME_KEY in tags:
    imgDateTimeStr = tags[IMG_DATETIME_KEY].values
    imgDateTime = datetime.strptime(imgDateTimeStr, '%Y:%m:%d %H:%M:%S')
    img_filename = imgDateTime.strftime('%Y%m%d_%H%M%S')
  if img_filename == '':
    raise Exception('Cannot read exif [%s] for file: %s' % (IMG_DATETIME_KEY, src_file))

  filename, file_extension = os.path.splitext(src_file)
  return img_filename, file_extension

def renameIMG(src_file):
  validate(src_file)
  new_filename, file_extension = getIMGFilename(src_file)
  new_filepath_noext = os.path.join(os.path.dirname(src_file), new_filename)
  new_filepath = new_filepath_noext + file_extension
  i = 1
  while os.path.isfile(new_filepath):
    new_filepath = new_filepath_noext + "_%d" % i + file_extension
    i += 1

  os.rename(src_file, new_filepath)
  return new_filename

def main():
  src_file = sys.argv[1]
  try:
    dst_file = renameIMG(src_file)
    return 0
  except Exception as e:
    print "Error: %s" % e.args
    return 1

if __name__ == '__main__':
  sys.exit(main())

