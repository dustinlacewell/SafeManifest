from random import choice
from string import ascii_letters

from safemanifest import SafeManifest, SafeManifestException 

def _get_random_filename():
    return ''.join(choice(ascii_letters) for x in range(5))

def test_non_existent_file():
    filename = _get_random_filename()

    try:
        manifest = SafeManifest(filename)
    except SafeManifestException, e:
        assert 'does not exist' in e.message
    else:
        assert False

def test_invalid_python():
    filename = _get_random_filename()
    with open(filename, 'w') as file:
        file.write(filename)

    try:
        manifest = SafeManifest(filename)
    except SafeManifestException, e:
        assert False
    except NameError:
        assert True
    else:
        assert False

def test_nonexistent_attrs_is_none():
    manifest = SafeManifest('safemanifest.py')
    assert getattr(manifest, _get_random_filename()) is None

def test_nonexistent_attrs_equal_false():
    manifest = SafeManifest('safemanifest.py')
    assert bool(getattr(manifest, _get_random_filename())) == False

def test_existing_attrs_are_valid():
    filename = _get_random_filename()
    with open(filename, 'w') as file:
        file.write("""qwerty = 'foobar'""")

    manifest = SafeManifest(filename)
    assert manifest.qwerty == 'foobar'

def test_module_attr_assignment_does_nothing():
    filename = _get_random_filename()
    with open(filename, 'w') as file:
        file.write("""qwerty = 'foobar'""")

    manifest = SafeManifest(filename)
    manifest.qwerty = 'zigzag'
    assert manifest.qwerty == 'foobar'
    
def test_nonmodule_attr_assignment_does_nothing():
    filename = _get_random_filename()
    with open(filename, 'w') as file:
        file.write("""qwerty = 'foobar'""")

    manifest = SafeManifest(filename)
    manifest.baghag = 'zigzag'
    assert manifest.baghag == None
    
    
