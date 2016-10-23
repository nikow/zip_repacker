#!/usr/bin/env python3
import os
import subprocess
import glob
from sevenzip_wrapper import SevenZip, SevenZipError

packer = SevenZip()
current_directory = os.getcwd()
print('Current directory %s' % current_directory)
zip_files = glob.glob('*.zip')
print('Found zips: %s' % zip_files)

for zipname in glob.glob('*.zip'):
    templorary_name = '%s_tmp' % zipname
    print('Unpacking zip %s to %s' % (zipname, templorary_name))
    try:
        packer.extract(zipPath=zipname, toPath=templorary_name)
    except SevenZipError as exc:
        print(exc)
    print('Removing zip file')
    os.remove(zipname)
    print('Changing directory to %s' % templorary_name)
    os.chdir(templorary_name)
    print('Compresing %s content to %s' % (templorary_name, zipname))
    try:
        packer.pack(zipPath=zipname, archivePath='*')
    except SevenZipError as exc:
        print(exc)
    os.chdir(current_directory)
    print('Comming back to %s' % current_directory)
    subprocess.run(['rm', '-rf', '%s' % templorary_name])
