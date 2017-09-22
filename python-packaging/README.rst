===================================
Packaging and Distributing Projects
===================================

This section covers the basics of how to configure, package and distribute your
own Python projects.

For more reference material, see `Building and Distributing Packages
<https://setuptools.readthedocs.io/en/latest/setuptools.html>`_ in the
`setuptools <https://pypi.python.org/pypi/setuptools>`_, but note that some
advisory content there may be outdated. In the event of conflicts, prefer
the advice in the Python Packaging User Guide.

.. contents:: Contents
   :local:

Requirements for Packaging and Distributing
===========================================

1. Install pip, setuptools, and wheel

* If you have Python 2 >=2.7.9 or Python 3 >=3.4 installed from `python.org
  <https://www.python.org>`_, you will already have ``pip`` and
  ``setuptools``, but will need to upgrade to the latest version:

  On Linux or OS X:

  ::

    pip install -U pip setuptools


  On Windows:

  ::

    python -m pip install -U pip setuptools

* If you're using a Python install on Linux that's managed by the system package
  manager (e.g "yum", "apt-get" etc...), and you want to use the system package
  manager to install or upgrade pip, then see `Installing
  pip/setuptools/wheel with Linux Package Managers`

* Otherwise:

 * Securely Download `get-pip.py
   <https://bootstrap.pypa.io/get-pip.py>`

 * Run ``python get-pip.py``. This will install or upgrade pip.
   Additionally, it will install ``setuptools`` and ``wheel`` if they're
   not installed already.

2. Requirements files

  ::

	pip install -r requirements.txt

3. (For debian distro only) Install depend package:

  ::

  	apt-get install python-stdeb fakeroot python-all -y


Configuring your Project
========================


Initial Files
-------------

setup.py
~~~~~~~~

The most important file is "setup.py" which exists at the root of your project
directory. For an example, see the `setup.py
<sampleproject/setup.py>`_.

"setup.py" serves two primary functions:

1. It's the file where various aspects of your project are configured. The
   primary feature of ``setup.py`` is that it contains a global ``setup()``
   function.  The keyword arguments to this function are how specific details of
   your project are defined.  The most relevant arguments are explained in
   ``the section below <setup() args>``.

2. It's the command line interface for running various commands that
   relate to packaging tasks. To get a listing of available commands, run
   ``python setup.py --help-commands``.

setup.cfg
~~~~~~~~~

"setup.cfg" is an ini file that contains option defaults for ``setup.py``
commands.  For an example, see the `setup.cfg <sampleproject/setup.cfg>`_.

README.rst
~~~~~~~~~~

All projects should contain a readme file that covers the goal of the
project. The most common format is `reStructuredText
<http://docutils.sourceforge.net/rst.html>`_. Another common format is `markdown
<https://daringfireball.net/projects/markdown/>`_.

MANIFEST.in
~~~~~~~~~~~

A "MANIFEST.in" is needed in certain cases where you need to package additional
files that ``python setup.py sdist (or bdist_wheel)`` don't automatically
include. To see a list of what's included by default, see the `Specifying the
files to distribute
<https://docs.python.org/3.4/distutils/sourcedist.html#specifying-the-files-to-distribute>`_.

For an example, see the `MANIFEST.in <sampleproject/MANIFEST.in>`_.

<your package>
~~~~~~~~~~~~~~

Although it's not required, the most common practice is to include your
python modules and packages under a single top-level package that has the same
`name <setup() name>`_ as your project, or something very close.

.. _`setup() args`:

setup() args
------------

As mentioned above, The primary feature of ``setup.py`` is that it contains a
global ``setup()`` function.  The keyword arguments to this function are how
specific details of your project are defined.

The most relevant arguments are explained below. The snippets given are taken
from the `setup.py <sampleproject/setup.py>`_.


.. _`setup() name`:

name
~~~~

::

  name='sample',

This is the name of your project.

version
~~~~~~~

::

  version='1.2.0',

This is the current version of your project, allowing your users to determine whether or not they have the latest version, and to indicate which specific versions they've tested their own software against.

description
~~~~~~~~~~~

::

  description='A sample Python project',
  long_description=long_description,

Give a short and long description for you project. 

author
~~~~~~

::

  author='The Python Packaging Authority',
  author_email='pypa-dev@googlegroups.com',

Provide details about the author.


license
~~~~~~~

::

  license='MIT',

Provide the type of license you are using.

classifiers
~~~~~~~~~~~

::

  classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',

      # Indicate who your project is intended for
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',

      # Pick your license as you wish (should match "license" above)
       'License :: OSI Approved :: MIT License',

      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
  ],

Provide a list of classifiers the categorize your project. For a full listing,
see https://pypi.python.org/pypi?%3Aaction=list_classifiers.

keywords
~~~~~~~~

::

  keywords='sample setuptools development',

List keywords that describe your project.


packages
~~~~~~~~

::

  packages=find_packages(exclude=['contrib', 'docs', 'tests*']),


It's required to list the ``packages <Import Package>`` to be included
in your project.  Although they can be listed manually,
``setuptools.find_packages`` finds them automatically.  Use the ``exclude``
keyword argument to omit packages that are not intended to be released and
installed.

install_requires
~~~~~~~~~~~~~~~~

::

 install_requires=['peppercorn'],

"install_requires" should be used to specify what dependencies a project
minimally needs to run. When the project is installed by ``pip``, this is the
specification that is used to install its dependencies.

.. _`Data Files`:

data_files
~~~~~~~~~~

::

    data_files=[('my_data', ['data/data_file'])],

Although configuring ``Package Data`` is sufficient for most needs, in some
cases you may need to place data files *outside* of your ``packages
<Import Package>``.  The ``data_files`` directive allows you to do that.

Each (directory, files) pair in the sequence specifies the installation
directory and the files to install there. If directory is a relative path, it is
interpreted relative to the installation prefix. Each file name in files is
interpreted relative to the ``setup.py`` script at the top of the project source
distribution.

scripts
~~~~~~~

Although ``setup()`` supports a `scripts
<http://docs.python.org/3.4/distutils/setupscript.html#installing-scripts>`_
keyword for pointing to pre-made scripts to install, the recommended approach to
achieve cross-platform compatibility is to use `console_scripts`_ entry
points (see below).

entry_points
~~~~~~~~~~~~

::

  entry_points={
    ...
  },


Use this keyword to specify any plugins that your project provides for any named
entry points that may be defined by your project or others that you depend on.

The most commonly used entry point is "console_scripts" (see below).

.. _`console_scripts`:

console_scripts
***************

::

  entry_points={
      'console_scripts': [
          'sample=sample:main',
      ],
  },

Use "console_script" `entry points
<https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins>`_
to register your script interfaces.

`Refs about 2 way to create Commandline scripts <https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html>`_.

Packaging your project
======================

To have your project installable from a Package Index like PyPI, you’ll need to create a Distribution (aka “Package” ) for your project.

Make Debian packages for a Python package
-----------------------------------------

You can generate both source and binary packages, like this:

::

  python setup.py --command-packages=stdeb.command bdist_deb

or you can generate source packages only, like this:

::

  python setup.py --command-packages=stdeb.command sdist_dsc

Make RPM packages for a Python package
-----------------------------------------

Similar with above section, let Python do this:

::

  python setup.py bdist_rpm


References
==========

1. `Python Package User Guide <https://packaging.python.org/>`_.

2. `Use stdeb to make Debian package for Python package <http://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html>`_.

3. `Make RPM package for Python package <http://shallowsky.com/blog/programming/packaging-python-rpm.html>`_.
