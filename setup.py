"""
Python AEMET Library
See:
https://packaging.python.org/en/latest/distributing.html
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'description.txt'), encoding='utf-8') as f:
    description = f.read()

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='python-aemet',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.2',

    description=description,
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/pablo-moreno/python-aemet',

    # Author details
    author='Pablo Moreno',
    author_email='pablomoreno.inf@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # OS
        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='aemet weather api spain opendata',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    include_package_data=True,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[requirements],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'aemet=aemet:main',
        ],
    },
    data_files=[(
        'aemet/data', [
            'aemet/data/cod_ccaa.json',
            'aemet/data/cod_ccaa.csv',
            'aemet/data/cod_costas.json',
            'aemet/data/cod_costas.csv',
            'aemet/data/cods_idema.json',
            'aemet/data/municipios.json',
            'aemet/data/municipios.csv',
            'aemet/data/estaciones_contaminacion.json',
            'aemet/data/estaciones_contaminacion.csv',
        ]
    )],
    package_data={
        'aemet/data': [
            'aemet/data/cod_ccaa.json',
            'aemet/data/cod_ccaa.csv',
            'aemet/data/cod_costas.json',
            'aemet/data/cod_costas.csv',
            'aemet/data/cods_idema.json',
            'aemet/data/municipios.json',
            'aemet/data/municipios.csv',
            'aemet/data/estaciones_contaminacion.json',
            'aemet/data/estaciones_contaminacion.csv',
        ]
    }
)
