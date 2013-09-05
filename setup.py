#! /usr/bin/env python3

from distutils.core import setup

setup (
    name="tvcmd",
    version="0.8.2",
    description="Command line tool to keep track of tv shows",
    author="Juan Tascón",
    author_email="juantascon@horlux.org",
    maintainer="Juan Tascón",
    maintainer_email="juantascon@horlug.org",
    url="https://sourceforge.net/projects/tvcmd/",
    keywords=["tvcmd", "episodes", "tv", "shows", "cli"],
    
    packages=["tvcmd"],
    scripts=["script/tvcmd"],
    data_files=[("share/tvcmd", ["README", "LICENSE", "TODO", "share/tvcmd.svg", "share/main.cfg.example"])],
    
    license="GPL, Version 3.0"
    )
