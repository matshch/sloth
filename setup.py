"""
sloth
-----

sloth is a tool for labeling image and video data for computer vision research.

The documentation can be found at http://sloth.readthedocs.org/ .

"""
import os
import os.path
import sys
from cx_Freeze import setup, Executable
from distutils.command.install import INSTALL_SCHEMES
import sloth

sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)))

# the following installation setup is based on django's setup.py
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
sloth_dir = 'sloth'

for dirpath, dirnames, filenames in os.walk(sloth_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
        if 'labeltool.ui' in filenames:
            data_files.append([dirpath, [os.path.join(dirpath, 'labeltool.ui')]])
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

build_exe_options = {
    'includes': ['numpy.core._methods',
                 'numpy.lib.format'],
    'include_msvcr': True,
    # optimize 2 breaks __doc__
    'optimize': 1
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name='sloth',
      version=sloth.VERSION,
      description='The Sloth Labeling Tool',
      author='CV:HCI Research Group',
      url='http://sloth.readthedocs.org/',
      requires=['importlib', 'PyQt4', 'numpy'],
      packages=packages,
      data_files=data_files,
      options = {'build_exe': build_exe_options},
      scripts=['sloth/bin/sloth'],
      executables = [Executable(script='sloth/bin/sloth',
                                icon='sloth/gui/icons/sloth.ico',
                                base=base,
                                shortcutName='Sloth',
                                shortcutDir='ProgramMenuFolder')]
)
