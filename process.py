#!/usr/bin/env python
# Need to copy all files back from sorted dirs and rerun with
# new date formats.

import os
import sys
import exifread
import time
import datetime
import shutil

print 'Processing pictures in:', str(sys.argv[1]), '\n'

walk_dir = sys.argv[1]

extensionsToCheck = ['.avi', '.mov', '.mts', '.mpg', '.jpg', '.jpeg', '.nef']
movieExtensions = ['.avi', '.mov', '.mts']

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    print('--\nroot = ' + root)




    for subdir in subdirs:
        print('\t- subdirectory ' + subdir)
        print(files)
    for currentFile in files:
          print('\t- file ' + currentFile)


          fileName, fileExtension = os.path.splitext(currentFile)
          if any(ext in fileExtension.lower() for ext in extensionsToCheck):

            fullName = os.path.join(root, currentFile)
            print fileName

            # Need to get this time into the same format as t
            creationTime = datetime.datetime.fromtimestamp(os.path.getmtime(fullName))
            dateName = ''
            if os.path.getmtime(fullName) < os.path.getctime(fullName):
              creationTime = datetime.datetime.fromtimestamp(os.path.getmtime(fullName))

            if fileExtension.lower() == '.jpg':
              # Try opening the exif data.
              f = open(fullName, 'rb')
              tags = exifread.process_file(f)
              d = tags.get('EXIF DateTimeOriginal', 'fail')
              f.close()
              if d != 'fail':
                print 'Using EXIF'
                creationTime = datetime.datetime.strptime(str(d), '%Y:%m:%d %H:%M:%S')

            if any(ext in fileExtension.lower() for ext in movieExtensions):
              # Create date string from time
              dateName = creationTime.strftime("%Y-%m-%d")
              dateName = 'vids/' + dateName
            else:
              # Create date string from time
              dateName = creationTime.strftime("%Y-%m-%d")
              dateName = 'pics/' + dateName

            # If the folder doesn't exist, create one
            if os.path.exists(dateName) == False:
              os.makedirs(dateName)

            # Move the file to the directory
            shutil.copy2(fullName, dateName+'/'+currentFile)
