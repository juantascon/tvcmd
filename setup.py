#! /usr/bin/env python3

from setuptools import setup

from tvcmd import __author__, __author_email__, __version__, __license__

setup (
    name="tvcmd",
    version=__version__,
    description="Command line tool to keep track of tv shows",
    url="http://tvcmd.horlux.org",
    author=__author__,
    author_email=__author_email__,
    maintainer=__author__,
    maintainer_email=__author_email__,
    license=__license__,
    keywords=["tvcmd", "episodes", "tv", "shows", "cli"],
    
    install_requires=[
        'pyxdg',
        'httplib2'
    ],
    
    packages=["tvcmd", "tvcmd.lib", "tvcmd.sources"],
    scripts=["script/tvcmd"],
    data_files=[("share/tvcmd", ["README.md", "LICENSE", "share/tvcmd.svg", "share/main.cfg.example"])]
)
