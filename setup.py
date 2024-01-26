from setuptools import setup

setup(
    name='otmantest-blendertoolbox',
    version='0.2.0',
    description='A example Python package',
    url='https://github.com/otmanon/BlenderToolbox.git',
    author='Hsueh-Ti Derek Liu',
    author_email='null@aol.com',
    license='Apache License 2.0',
    packages=['BlenderToolbox'],
    install_requires=[
                      'bpy==4.0',
                      'numpy',
                      ],

    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)