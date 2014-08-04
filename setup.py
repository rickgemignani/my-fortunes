#!/usr/bin/python2.5
#encoding=utf-8

'''
    DONT TOUCH THIS FILE, UNLESS YOU KNOW WHAT YOU ARE DOING !!!
    Modify the release.cfg under the project module in config folder instead.
'''

import os
release_file = None
for root, dirs, files in os.walk(u'.'):
    if u'release.py' in files:
        release_file = os.path.join(root, u'release.py')
        execfile(release_file)
        break;

if release_file is None:
    raise IOError, 'Release File not found!'

from setuptools import setup, find_packages
from turbogears.finddata import find_package_data
packages=find_packages()
package_data = find_package_data(where=short_name, package=package_name)

for data_dir in data_dirs:
    if os.path.isdir(data_dir):
        packages.append(data_dir)
        package_data.update(find_package_data(where=data_dir, only_in_packages=False))

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    url=url,
    download_url=download_url,
    license=license,
    install_requires=install_requires,
    zip_safe=zip_safe,
    packages=packages,
    package_data=package_data,
    keywords=keywords,
    classifiers=classifiers,
    test_suite=test_suite,
    entry_points=entry_points,
    data_files=data_files,
)
