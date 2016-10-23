import subprocess
import distutils.spawn


class SevenZipError(Exception):
    '''Generic error class for 7z command line operations.'''

    def __init__(self, msg='7z: Unknown Error'):
        self.value = msg

    def __str__(self):
        return repr(self.value)


class FatalError(SevenZipError):
    '''Error class for 7z fatal error return code.'''

    def __init__(self, msg='7z: Fatal Error'):
        self.value = msg


class CommandLineError(SevenZipError):
    '''Error class for 7z commmand line error return code.'''

    def __init__(self, msg='7z: Command Line Error'):
        self.value = msg


class MemError(SevenZipError):
    '''Error class for 7z memory error return code.'''

    def __init__(self, msg='7z: Not enough memory to perform this operation'):
        self.value = msg


class UserInterrupt(SevenZipError):
    '''Error class for 7z user interruption return code.'''

    def __init__(self, msg='7z: Process interrupted by user'):
        self.value = msg


class SevenZip(object):
    @property
    def packer_path(self):
        path = distutils.spawn.find_executable('7z')
        if path is None:
            raise EnvironmentError('Packer class can not find 7z executable')
        return path

    def run(self, command):
        # subp = subprocess.Popen(
        #     command, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        # )
        subp = subprocess.Popen(command)
        result = subp.wait()

        if result == 0:
            return True
        elif result == 1:
            return False
        elif result == 2:
            raise FatalError
        elif result == 7:
            raise CommandLineError
        elif result == 8:
            raise MemError
        elif result == 255:
            raise UserInterrupt
        else:
            raise SevenZipError

    def extract(self, zip_path, to_path=''):
        assert zip_path, (
            'Packer extract function need path from '
            'which it will be extracting.'
        )
        if not to_path:
            to_path = zip_path + '_TMP'
        command = [self.packer_path, 'x', '-y',
                   '-o%s' % to_path, '%s' % zip_path]
        command_result = self.run(command)
        return command_result

    def pack(self, zip_path, archive_path='*'):
        assert zip_path, 'Packed zip must have name'
        assert archive_path, 'There must be source of zip, right?'
        command = [self.packer_path, 'a', '-tzip',
                   '-mx=9', '../%s' % zip_path, archive_path]
        command_result = self.run(command)
        return command_result
