"""Setup for Troweb XBlock."""

import os

from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='troweb-xblock',
    author='edSpirit',
    author_email='developers@edspirit.com',
    version='0.1',
    description='Troweb XBlock',
    license='AGPL v3',
    url='https://github.com/Edspirit/xblock-troweb',
    packages=[
        'troweb_xblock',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'troweb_xblock = troweb_xblock:TrowebXBlock',
        ]
    },
    package_data=package_data("troweb_xblock", ["static", "public"]),
)
