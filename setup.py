#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re
from setuptools import setup

VERSIONFILE = "ncml/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')
LICENSE = read('LICENSE')

FILL_ME = 'None'

source = 'http://pypi.python.org/packages/source'
install_requires = None

classifiers = """\
Development Status :: 1 - Planning
Environment :: Console
Intended Audience :: Science/Research
Intended Audience :: Developers
Intended Audience :: Education
License :: OSI Approved :: CC License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering
"""

config = dict(name='ncml',
              version=verstr,
              packages=['ncml'],
              test_suite='tests',
              use_2to3=True,
              license=LICENSE,
              long_description=long_description,
              classifiers=filter(None, classifiers.split("\n")),
              description='Python tools for manipulating NCML (NetCDF Markup)',
              author=FILL_ME,
              author_email=FILL_ME,
              maintainer=FILL_ME,
              maintainer_email=FILL_ME,
              url='http://pypi.python.org/pypi/ncml/',
              download_url='%s/n/ncml/ncml-%s.tar.gz' % (source, verstr),
              platforms='any',
              keywords=[FILL_ME, FILL_ME, FILL_ME],
              install_requires=install_requires)

setup(**config)
