#!/usr/bin/env python
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='frisbee',
    version='0.0.3',
    description='Search tool to find email addresses by abusing search',
    url="https://github.com/9b/frisbee",
    author="Brandon Dixon",
    author_email="brandon@9bplus.com",
    license="MIT",
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests', 'requests-futures',
                      'namesgenerator'],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries'
    ],
    entry_points={
        'console_scripts': [
            'frisbee = frisbee.cli.client:main'
        ]
    },
    zip_safe=False,
    keywords=['emails', 'leads', 'search engine', 'crawler', 'intel'],
    download_url='https://github.com/9b/frisbee/archive/master.zip'
)
