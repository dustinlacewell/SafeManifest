
SafeManifest
============

**SafeManifest** is a simple object providing easy access to configuration files that are written as Python scripts. It will perform the import of the file and provide you attributes that map to the module-level attributes of the config file. **It is safe, only in the fact that missing expected options in the target config return None instead of AttributeErrors.** This allows you to test whether the user has defined certain options (module level attributes) with a conditional instead of a try/except.:


    >>> from safemanifest import SafeManifest
    >>> m = SafeManifest('/home/dlacewell/.cage')
    >>> m.servers
    {'cage': {'cageroot': '/var/www', 'user': 'vagrant', 'address': '33.33.33.33'}}


Any attributes that don't exist will return None:


    >>> m.foobar
    >>> repr(m.foobar)
    'None'


and setting any attribute will do nothing.


    >>> m.servers = None
    >>> m.servers
    {'cage': {'cageroot': '/var/www', 'user': 'vagrant', 'address': '33.33.33.33'}}
    >>> m.foobar = 0
    >>> repr(m.foobar)
    'None'


Ofcourse changing attributes of existing attributes works like normal:


    >>> m.servers['cage']['user']
    vagrant
    >>> m.servers['cage']['user'] = 'otheruser'
    >>> m.servers['cage']['user']
    otheruser





