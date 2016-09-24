#!/usr/bin/env python3
import os
import subprocess
import glob


def run(command):
    print('Calling command: %s' % command)
    subprocess.run(command, check=True)


current_directory = os.getcwd()
print('Current directory %s' % current_directory)
zip_files = glob.glob('*.zip')
print('Found zips: %s' % zip_files)

for zipname in glob.glob('*.zip'):
    templorary_name = '%s_tmp' % zipname
    print('Unpacking zip %s to %s' % (zipname, templorary_name))
    run(['7z', 'x', '-y', '-o%s' % templorary_name, '%s' % zipname])
    print('Removing zip file')
    os.remove(zipname)
    print('Changing directory to %s' % templorary_name)
    os.chdir(templorary_name)
    print('Compresing %s content to %s' % (templorary_name, zipname))
    run(['7z', 'a', '-tzip', '-mx=9', '../%s' % zipname, '*'])
    os.chdir(current_directory)
    print('Comming back to %s' % current_directory)
    run(['rm', '-rf', '%s' % templorary_name])
