#!/usr/bin/env bash

# 0. [OPTIONAL] Remove all files from dist/
sudo rm dist/*

# 1. Create distribution file
sudo python3 setup.py sdist bdist_wheel

# 2. Upload to Pypi
twine upload dist/*
