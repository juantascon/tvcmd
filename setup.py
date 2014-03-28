#! /usr/bin/env python3

from distutils.core import setup

from tvcmd import __author__, __author_email__, __version__, __license__

setup (
    name="tvcmd",
    version=__version__,
    description="Command line tool to keep track of tv shows",
    author=__author__,
    author_email=__author_email__,
    maintainer=__author__,
    maintainer_email=__author_email__,
    url="http://tvcmd.horlux.org",
    keywords=["tvcmd", "episodes", "tv", "shows", "cli"],
    
    packages=["tvcmd", "tvcmd.lib", "tvcmd.sources"],
    scripts=["script/tvcmd"],
    data_files=[("share/tvcmd", ["README.md", "LICENSE", "share/tvcmd.svg", "share/main.cfg.example"])],
    
    license=__license__
)
