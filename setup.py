#! /usr/bin/env python3

from distutils.core import setup

setup (
    name="tvcmd",
    version="0.9",
    description="Command line tool to keep track of tv shows",
    author="Juan Tascon",
    author_email="juantascon@horlux.org",
    maintainer="Juan Tascón",
    maintainer_email="juantascon@horlug.org",
    url="http://tvcmd.horlux.org",
    keywords=["tvcmd", "episodes", "tv", "shows", "cli"],
    
    packages=["tvcmd", "tvcmd.lib", "tvcmd.sources"],
    scripts=["script/tvcmd"],
    data_files=[("share/tvcmd", ["README", "LICENSE", "share/tvcmd.svg", "share/main.cfg.example"])],
    
    license="GPL, Version 3.0"
)
