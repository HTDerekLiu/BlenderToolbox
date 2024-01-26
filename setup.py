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

__version__ = '0.11.0'





def main():
    with open('README.md') as f:
        long_description = f.read()

    # ... other setup parameters


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

    try:
        from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
        class bdist_wheel(_bdist_wheel):
            def finalize_options(self):
                _bdist_wheel.finalize_options(self)
                self.root_is_pure = False
    except ImportError:
        bdist_wheel = None

    setup(
        name='otmantest-blendertoolbox',
        version=__version__,
        author='Hsueh-Ti Derek Liu',
        author_email='sample@aol.edu',
        url='https://github.com/otmanon/BlenderToolbox',
        python_requires='>=3.10',
        description='Blender Toolbox.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license="Apache 2.0",
        install_requires=[],
        package_dir={'': 'BlenderToolBox'},
        packages=setuptools.find_packages(where="BlenderToolBox"),
        # options={"bdist_wheel": {"python_tag": "cp310"}},
        zip_safe=False,
    )


if __name__ == "__main__":
    main()