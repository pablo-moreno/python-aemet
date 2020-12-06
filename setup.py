"""
Python AEMET Library
See:
https://packaging.python.org/en/latest/distributing.html
"""
from setuptools import setup, find_packages
from os import path, environ

here = path.abspath(path.dirname(__file__))
description = 'Cliente de la API de datos de AEMET'

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='python-aemet',
    version='0.3.4',
    description=description,
    long_description=long_description,
    url='https://github.com/pablo-moreno/python-aemet',
    author='Pablo Moreno',
    author_email='pablomoreno.inf@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='aemet weather api spain opendata',
    include_package_data=True,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[requirements],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
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
