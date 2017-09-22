#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()


requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='simple_python_package',
    version='0.1.0',
    description="Short description about ",
    long_description=readme,
    author="Nguyen Tuan Kien",
    author_email='ntk148v@gmail.com',
    url='https://github.com/ntk148v/python_packaging/simple_python_package',
    packages=[
        'simple_python_package',
    ],
    package_dir={'simple_python_package':
                 'simple_python_package'},
    entry_points={
        'console_scripts': [
            'simple_python_package=simple_python_package.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='simple_python_package',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    tests_require=test_requirements
)
