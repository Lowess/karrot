#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

# Setup requirements
try:
    from setuptools import setup, find_packages
    from setuptools.command.install import install
except ImportError:
    print(
        "setuptools is needed in order to build. Install it using your package manager (usually python-setuptools) or via pip (pip install setuptools)."
    )
    sys.exit(1)


def read_file(file_name):
    """Read file and return its contents."""
    with open(file_name, "r") as f:
        return f.read()


def parse_release():
    release_py = read_file("karrot/release.py")
    version = re.search(r'__version__ = "(.*?)"', release_py).group(1)
    author = re.search(r'__author__ = "(.*?)"', release_py).group(1)
    email = re.search(r'__email__ = "(.*?)"', release_py).group(1)
    return (version, author, email)


__version__, __author__, __email__ = parse_release()


def get_dynamic_setup_params():
    """Add dynamically calculated setup params to static ones."""

    return {
        # Retrieve the long description from the README
        "long_description": read_file("README.md")
    }


# Inspired from https://circleci.com/blog/continuously-deploying-python-packages-to-pypi-with-circleci/
class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "Verify that the git tag matches the version"

    def run(self):
        tag = os.getenv("DRONE_TAG", "unknown")

        if tag != __version__:
            info = "Git tag: {} does not match the version of this app: {}".format(
                tag, __version__
            )
            sys.exit(info)


# Extra requirements installable using pip -e '.[<extra>]'
EXTRAS_REQUIRE = {
    "docs": ["sphinx", "sphinxcontrib.mermaid>=0.3.1", "sphinx-rtd-theme>=0.4.3"],
    "tests": [
        "tox",
        "black",
        "moto>=1.3.14",
        "coverage-badge>=1.0.1",
        "coverage>=4.5.4",
        "flake8>=3.7.9",
        "pytest-cov>=2.8.1",
        "pytest-runner>=5.2",
        "pytest-flask>=0.15.0",
        "pytest-datafiles>=2.0",
        "pytest>=5.2.2",
    ],
}

# Development requirements
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["docs"] + ["pre-commit"]
)

static_setup_params = dict(
    name="karrot",
    version=__version__,
    description=(
        "Karrot lag reporting tool for Prometheus and Cloudwatch ingesting events from Burrow"
    ),
    keywords="kafka,burrow,prometheus,aws,cloudwatch",
    author=__author__,
    author_email=__email__,
    url="https://github.com/Lowess/karrot",
    package_dir={"": "karrot"},
    packages=find_packages(""),
    package_data={},
    zip_safe=False,
    scripts=[],
    license="Apache License 2.0",
    install_requires=[
        "structlog>=19.1.0",
        "Flask>=1.0",
        "munch>=2.5.0",
        "prometheus_client>=0.7.1",
        "boto3>=1.10.0",
        "python-dateutil==2.8.0",
        "gunicorn>=19.8.0,<20.0",
    ],
    extras_require=EXTRAS_REQUIRE,
    test_suite="test",
    cmdclass={"verify": VerifyVersionCommand},
)


if __name__ == "__main__":
    setup_params = dict(static_setup_params, **get_dynamic_setup_params())
    setup(**setup_params)
