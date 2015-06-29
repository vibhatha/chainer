#!/usr/bin/env python
import os
import os.path
import urllib
import zipfile


urllib.urlretrieve(
    'http://nlp.stanford.edu/sentiment/trainDevTestTrees_PTB.zip',
    'trainDevTestTrees_PTB.zip')
zf = zipfile.ZipFile('trainDevTestTrees_PTB.zip')
for name in zf.namelist():
    (dirname, filename) = os.path.split(name)
    if not filename == '':
        zf.extract(name, '.')
