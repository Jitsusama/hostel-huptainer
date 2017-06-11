"""PIP Project Installation Program."""

from setuptools import setup, find_packages
try:
    from hostel_huptainer import __version__
except ImportError:
    import os
    import sys
    path = os.path.dirname(__file__)
    sys.path.insert(0, '{}/source'.format(path))
    print(sys.path)
    from hostel_huptainer import __version__

setup(
    name='hostel-huptainer',
    version=__version__,
    license='Apache-2.0',
    author='Joel Gerber',
    author_email='joel@grrbrr.ca',
    url='https://github.com/jitsusama/hostel-huptainer',
    download_url=(
        'https://github.com/jitsusama/hostel-huptainer/releases'
        '/download/v{0}/hostel-huptainer-{0}.tar.gz'.format(__version__)),
    keywords=['Docker'],
    description=(
        "SIGHUP docker container processes that have a HOSTNAME label "
        "matching a supplied string."),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages=find_packages('source'),
    package_dir={'': 'source'},
    entry_points={
        'console_scripts': [
            'hostel-huptainer = hostel_huptainer.__main__:main'
        ]
    },
    install_requires=['docker'],
    tests_require=[
        'pylama',
        'pylama_pylint',
        'pytest',
        'pytest-cov',
        'pytest-mock',
        'docker',
    ]
)
