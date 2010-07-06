# Copyright (c) 2010 Simplistix Ltd
# See license.txt for license details.

import os
from setuptools import setup, find_packages

package_name = 'execute'
version = '1.0'
base_dir = os.path.dirname(__file__)

setup(
    name=package_name,
    version=version,
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description="Common patterns for executing commands as sub processes",
    long_description=open(os.path.join(base_dir,'docs','description.txt')).read(),
    url='http://packages.python.org/execute',
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    ],    
    packages=find_packages(),
    zip_safe=False,
    extras_require=dict(
        test=[
            'manuel',
            'mock',
            'testfixtures',
            ],
        )
    )
