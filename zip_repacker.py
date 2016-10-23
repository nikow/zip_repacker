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

for zip_name in glob.glob('*.zip'):
    templorary_name = '%s_tmp' % zip_name
    print('Unpacking zip %s to %s' % (zip_name, templorary_name))
    try:
        packer.extract(zip_path=zip_name, to_path=templorary_name)
    except SevenZipError as exc:
        print(exc)
        break

    print('Removing zip file')
    os.remove(zip_name)
    print('Changing directory to %s' % templorary_name)
    os.chdir(templorary_name)
    print('Compresing %s content to %s' % (templorary_name, zip_name))
    try:
        packer.pack(zip_path=zip_name, archive_path='*')
    except SevenZipError as exc:
        print(exc)
        break
    os.chdir(current_directory)
    print('Comming back to %s' % current_directory)
    subprocess.run(['rm', '-rf', '%s' % templorary_name])
