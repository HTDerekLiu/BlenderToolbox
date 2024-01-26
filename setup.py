# This is essentially lifted from https://raw.githubusercontent.com/nmwsharp/polyscope-py/master/setup.py
# Thanks, Nick!
import os
import re
import sys
import platform
import subprocess
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

__version__ = '0.3.0'


class CMakeExtension(Extension):
    # Boilerplate that I don't fully understand
    def __init__(self, name, sourcedir='', exclude_arch=False):
        Extension.__init__(self, name, sources=[])
        # Directory where my python package is
        self.sourcedir = os.path.abspath(sourcedir)
        self.exclude_arch = exclude_arch




def main():
    with open('README.md') as f:
        long_description = f.read()

    # Applies to windows only.
    # Normally, we set cmake's -A option to specify 64 bit platform when need (and /m for build),
    # but these are errors with non-visual-studio generators. CMake does not seem to have an idiomatic
    # way to disable, so we expose an option here. A more robust solution would auto-detect based on the
    # generator.  Really, this option might be better titled "exclude visual-studio-settings-on-windows"
    if "--exclude-arch" in sys.argv:
        exclude_arch = True
        sys.argv.remove('--exclude-arch')
    else:
        exclude_arch = False

    setup(
        name='otmantest-blendertoolbox',
        version=__version__,
        author='Hsueh-Ti Derek Liu',
        author_email='sample@aol.edu',
        url='',
        description='Blender TOolbox.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license="Apache 2.0",
        package_dir={'': 'BlenderToolbox'},
        packages=setuptools.find_packages(where="BlenderToolbox"),
        install_requires=['numpy', 'bpy==4.0'],
        setup_requires=['bpy==4.0'],
        zip_safe=False,
    )


if __name__ == "__main__":
    main()