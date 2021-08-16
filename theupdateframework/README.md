# The Update Framework - TUF

https://theupdateframework.com/

- [The Update Framework - TUF](#the-update-framework---tuf)
  - [1. Overview](#1-overview)

## 1. Overview

- TUF helps developers maintain the security of _software update systems_, providing protection even against attackers that compromise the repository or signing keys.
- Software update systems is an application (or part of an application) running on a client system that obtains and installs software. Three major classes of software update systems are:
  - Application updaters which are used by applications to update themselves. For example, Firefox updates itself through its own application updater.
  - Library package managers such as those offered by many programming languages for installing additional libraries. These are systems such as Python's pip/easy_install + PyPI, Perl's CPAN, Ruby's RubyGems, and PHP's Composer.
  - System package managers used by operating systems to update and install all of the software on a client system. Debian's APT, Red Hat's YUM, and openSUSE's YaST are examples of these.
- The update procedure followed by a software update system can be regarded as straightforward:
  - Knowing when an update exists. (**TUF**)
  - Downloading the update. (**TUF**)
  - Applying the changes introduced by the update.

- TUF adds extra **metadata files** in repository which contain additional information: which keys are trusted, the cryptographic hashes of files, signatures on the metadata, metadata version numbers, and the date after which the metadata should be considered expired.

![](images/flow.png)
