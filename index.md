---
layout: tvcmd
---

## About:

tvcmd is a command line interface (CLI) to keep track of tv shows and episodes.
It is similar to websites such as myepisodes.com followmy.tv or mytvshows.org
but for the command line, allowing greater flexibility like automatic
torrent urls.

## Screenshots:

* [shell mode](https://raw.githubusercontent.com/juantascon/tvcmd/gh-pages/img/screenshot.png)

## Features:

* Gather show information such as dates, names, etc from several sources: tvrage.com, thetvdb.com
* Track only the shows you watch by editing a configuration file
* Track the status of episodes: new &#10137; adquired &#10137; seen
* Print each show in whichever format you like, handy for generating torrent links

## Configuration:

The main configuration file is located at `.config/tvcmd/main.cfg`, it is an ini style file
composed of three subsections inside a `general` section.

Example:

``` ini
[general]
source = tvrage
shows = friends, scrubs, firefly, attack_on_titan, the_ricky_gervais_show
formats =
  https://torrentz.eu/verifiedP?f=${show+}+s${season}e${episode},
  http://fenopy.se/search/${show+}+s${season}e${episode}.html?quality=1&order=1
```

The first subsection `source` defines which api use to query episodes information, at the
moment tvcmd supports: [tvrage](http://www.tvrage.com/) and [thetvdb](http://thetvdb.com/).

The second subsections `shows` is probably the most important as it is the list of shows to follow.
The list is separated by comma and the show names are lower case letters, numbers and/or the
underscore symbol, ex: friends, attack_on_titan, steins_gate, marvels_agents_of_s_h_i_e_l_d_,
the_office_us, cosmos_a_spacetime_odyssey, be careful though as some shows have different names
depending on the `source`. You can find out the exact name of a show by typing the command
`search` followed by a pattern, ex: `search the offi`

Finally, the optional subsection `formats` contains a list of strings, useful for automatic
torrent url generation. The following expressions are automatically replaced for each episode:

* `${show}`: full show name
* `${show+}`: same as above but with the + symbol instead of spaces
* `${season}`: season number (2 decimals)
* `${episode}`: episode number (2 decimals)

## Usage

tvcmd can be run in either command mode:

``` bash
$ tvcmd -e "ls friends.s0*"
```

or shell mode:

``` bash
$ tvcmd
tvcmd> ls friends.s0*
```

## Real Case Execution

Let's say we enjoy watching these shows: Friends, Scrubs and Attack On Titan.

Being by creating a basic configuration file:

``` ini
[general]
source = thetvdb
shows = friends, scrubs, attack_on_titan
formats = http://fenopy.se/search/${show+}+s${season}e${episode}.html?quality=1&order=1
```

Run the tvcmd in shell mode and execute the following secuence of commands:

``` bash
tvcmd> update
tvcmd> ls
tvcmd> format
```

Here `update` will query the source with your show list from your config file, 
`ls` will display the gathered episodes and `format` will print urls to download
torrent files from fenopy.se, `format` can also be executed using the `-f` option:

``` bash
$ tvcmd -f
```

Allowing greater flexibility:

``` bash
$ firefox $(tvcmd -f "friends.s01*" |grep fenopy.se)
```

Both `format` and `ls` receive a pattern to identify episodes, this pattern is
{showname}.s{season#}e{episode#}, ex: friends.s01e01, scrubs.s03e21,
steins_gate.s01e10 or to select many: friends.s01e0* scrubs.*, steins_gate.s0*.

By default every new episode is marked as `new`, once you download an episode
you can marked them as adquired with the `adquire` command and when you see it
you can mark it as seen with the `see` command. Episodes always follow this
secuence: new &#10137; adquired &#10137; seen.

Going back to our example once we have downloaded the episodes we can mark them
as adquired so they won't show up again with `format`:

``` bash
tvcmd> adquire friends.s01*
tvcmd> format
```

Or as seen and they won't show up again with `ls`:

``` bash
tvcmd> see friends.s01*
tvcmd> ls
```

For further information run `tvcmd -e help` or in shell mode `help` and `COMMAND -h`.
