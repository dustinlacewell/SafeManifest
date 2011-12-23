import pdb
import os, imp

class SafeManifestException(Exception): pass

class SafeManifest(object):
    def __init__(self, filename):
        self._module = self._load_real_module(filename)

    def __getattribute__(self, attr):
        '''
        Find attr on module or return None.

        (thanks to lahwran for helping getting this just right)
        '''
        try:
            obj = object.__getattribute__(self, '_module')
            if hasattr(obj, attr):
                return getattr(obj, attr)
        except AttributeError:
            return object.__getattribute__(self, attr)

    def _get_suffix(self):
        '''
        Get the filemode for .py
        '''
        for suffix in imp.get_suffixes():
            if '.py' in suffix:
                return suffix
        return ('.py', 'U', 1)

    def _load_real_module(self, filename):
        '''
        Load the actual module.
        '''
        # check if file exists
        if not os.path.isfile(filename):
            raise SafeManifestException(
                'The config module "{path}" does not exist.'.format(path=filename))
        # get the suffix and open te file
        suffix = self._get_suffix()
        try:
            file = open(filename, suffix[1])
        except IOError, e:
            raise SafeManifestException('%s : %s' % e.filename, e.strerror)
    
        try: # try to import the conf module
            module = imp.load_module('module', file, file.name, suffix)
        except ImportError, e: # reraise ImportError as our own
            raise SafeManifestException(
                'Unable to import "{path}": {error}'.format(path=file.name,
                                                            error=e.message))
        else: # otherwise return the conf module
            return module
        finally: # don't forget to close the file!
            file.close()

