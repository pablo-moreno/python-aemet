# 1. Create distribution file
sudo python3.5 setup.py sdist

# 2. Upload to Pypi
sudo twine upload dist/*
