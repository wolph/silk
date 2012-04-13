import os
import re
from setuptools import setup

if os.path.isfile('README.rst'):
    long_description = open('README.rst').read()
else:
    long_description = 'See http://pypi.python.org/pypi/silk/'

def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links

setup(
    install_requires = parse_requirements('requirements.txt'),
    dependency_links = parse_dependency_links('requirements.txt'),
    name = 'silk',
    version = '0.1',
    author = 'Rick van Hattem',
    author_email = 'Rick.van.Hattem@Fawo.nl',
    description = '''Silk is a django app that gives you a simple interface
        to deploy and/or rollback to your servers.''',
    url='https://github.com/WoLpH/silk',
    license = 'BSD',
    packages=['silk'],
    long_description=long_description,
    test_suite='nose.collector',
    setup_requires=['nose'],
    tests_require=['django'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
    ],
)

