# Sematic Versioning 2.0.0

Authored by [Tom Preston-Werner](http://tom.preston-werner.com/).

[Source](https://semver.org/)

## Introduction

* Dependency hell: the bigger your system grows and the more packages you integrate into your software, the more likely you are to find yourself, one day, in this put of despair.
    * Dependency specifications are too tight -> version lock (the inability to upgrade a package without having to release new versions of every dependent package).
    * Dependency specifications are too loosely -> version promiscuity (assuming compatibility with more future versions than is reasonable).

* Solution: A simple set of rules and requirements that dictate how version numbers are assigned and incremented -> Sematic Versioning (SemVer).

## Sematic Versioning (SemVer)

### Version Format

![](https://cdncontribute.geeksforgeeks.org/wp-content/uploads/semver.png)

```
MAJOR.MINOR.PATCH
```
* MAJOR version when you make incompatible API changes.
* MINOR version when you add functionality in a backwards-compatible manner.
* PATCH version when you make backwards-compatible bug fixes.

### Rules

1. Softaware using SemVer *MUST* declare a public API.

2. A normal version number *MUST* take the form X.Y.Z where X, Y and Z are non-negative integers, and *MUST NOT* contain leading zeroes. Each element *MUST* increase numerically.

3. Once a versioned package has been released, the contents of that version *MUST NOT* be modified. Any modifications *MUST* be released as a new version.

4. Major version (0.y.z) is for initial development. Anything may change at any time. The public API should not be considered stable.

5. Version 1.0.0 defines the public API. The way in which the version number is incremented after this release is dependent on this public API and how it changes.

6. Patch version Z (x.y.Z | x > 0) *MUST* be incremented if only backwards compatible bug fixes are introduced. A bug fix is defined as an internal change that fixes incorrect behavior.

7. Minor version Y (x.Y.z | x > 0) *MUST* be incremented if new, backwards compatible functionality is introduced to the public API. It *MUST* be incremented if any public API functionality is marked as deprecated. It *MAY* be incremented if substantial new functionality or improvements are introduced within the private code. It *MAY* include patch level changes. Patch version *MUST* be reset to 0 when minor version is incremented.

8. Major version X (X.y.z | X > 0) *MUST* be incremented if any backwards incompatible changes are introduced to the public API. It *MAY* include minor and patch level changes. Patch and minor version *MUST* be reset to 0 when major version is incremented.

9. A pre-release version *MAY* be denoted by appending a hyphen and a series of dot separated identifiers immediately following the patch version. Identifiers *MUST* comprise only ASCII alphanumerics and hyphen [0-9A-Za-z-]. Identifiers *MUST NOT* be empty. Numeric identifiers *MUST NOT* include leading zeroes. Pre-release versions have a lower precedence than the associated normal version. A pre-release version indicates that the version is unstable and might not satisfy the intended compatibility requirements as denoted by its associated normal version. Examples: 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7, 1.0.0-x.7.z.92.

10. Build metadata *MAY* be denoted by appending a plus sign and a series of dot separated identifiers immediately following the patch or pre-release version. Identifiers *MUST* comprise only ASCII alphanumerics and hyphen [0-9A-Za-z-]. Identifiers *MUST NOT* be empty. Build metadata *SHOULD* be ignored when determining version precedence. Thus two versions that differ only in the build metadata, have the same precedence. Examples: 1.0.0-alpha+001, 1.0.0+20130313144700, 1.0.0-beta+exp.sha.5114f85.

11. Precedence refers to how versions are compared to each other when ordered. Precedence *MUST* be calculated by separating the version into major, minor, patch and pre-release identifiers in that order (Build metadata does not figure into precedence). Precedence is determined by the first difference when comparing each of these identifiers from left to right as follows: Major, minor, and patch versions are always compared numerically. Example: 1.0.0 < 2.0.0 < 2.1.0 < 2.1.1. When major, minor, and patch are equal, a pre-release version has lower precedence than a normal version. Example: 1.0.0-alpha < 1.0.0. Precedence for two pre-release versions with the same major, minor, and patch version *MUST* be determined by comparing each dot separated identifier from left to right until a difference is found as follows: identifiers consisting of only digits are compared numerically and identifiers with letters or hyphens are compared lexically in ASCII sort order. Numeric identifiers always have lower precedence than non-numeric identifiers. A larger set of pre-release fields has a higher precedence than a smaller set, if all of the preceding identifiers are equal. Example: 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0.
