# tvcmd

## About:

Tvcmd is a command line interface (CLI) to keep track of tv shows episodes.
It is similar to websites such as myepisodes.com followmy.tv or mytvshows.org
but for the command line, allowing greater flexibility like automatic
torrent urls.

## Features:

* Gather show information such as dates, names, etc from several sources: tvrage.com, thetvdb.com
* Track only the shows you watch by editing a configuration file
* Track the status of episodes: new -> adquired -> seen
* Print each show in whichever format you like, handy for generating torrent links

## Configuration:

Create a configuration file on .config/tvcmd/main.cfg:

    $ source = tvrage
    $ shows = friends, scrubs, firefly, attack_on_titan, the_ricky_gervais_show
    $ formats =
    $   https://torrentz.eu/verifiedP?f=${show+}+s${season}e${episode},
    $   http://fenopy.se/search/${show+}+s${season}e${episode}.html?quality=1&order=1

## Usage

Start the tvcmd shell:

    $ tvcmd

Inside the tvcmd shell run update to gather the information from the source:

    $ update

Make sure it gathered the episodes of your shows:

    $ ls

Try generating the urls to search for torrents, this can be done inside the shell:

    $ format

Or more programmatically from bash:

    $ tvcmd -f

Allowing greater flexibility:

    $ firefox $(tvcmd -f |grep fenopy.se)

You can then mark episodes as adquired so they won't show up again with format:
  
    $ adquire friens.s01*
    $ format

Or as seen so they won't show up again with ls:

    $ see scrubs.s01e0*
    $ ls

For more info visit the official website: http://tvcmd.horlux.org
