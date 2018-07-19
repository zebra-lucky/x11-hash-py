# -*- coding: utf-8 -*-

import sys
from setuptools import setup


description='Pure python x11_hash implementation'
requirements = []
if sys.version_info.major < 3:
    requirements.append('future')

setup(
    name='x11-hash-py',
    version='0.1.0b1',
    install_requires=requirements,
    packages=[
        'x11_hash_py'
    ],
    package_dir={
        'x11_hash_py': 'x11_hash_py',
    },
    test_suite='x11_hash_py.tests.test_hashes',
    description=description,
    maintainer='zebralucky',
    maintainer_email='zebra.lucky@gmail.com',
    license='MIT License',
    url='https://github.com/zebra-lucky/x11-hash-py',
)
