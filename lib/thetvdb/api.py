#! /usr/bin/env python

import httplib2
import xml.etree.cElementTree as ElementTree

APIKEY = "FD9D34DB64F25A09"

def _get_url(url):
    h = httplib2.Http(cache = "/tmp/tvcmd-cache")
    resp, content = h.request(url, "GET")
    str_content = content.decode("utf-8")
    return str_content

def get_show_id(name):
    url = "http://thetvdb.com/api/GetSeries.php?seriesname=%s" % (name)
    response = _get_url(url)
    root = ElementTree.XML(response)
    series = list(root)[0]
    
    for s in list(series):
        if s.tag == "seriesid":
            return s.text
    return None
    
def get_episodes(name):
    id = get_show_id(name)
    
    url = "http://thetvdb.com/api/%s/series/%s/all/en.xml" % (APIKEY, id)
    response = _get_url(url)
    root = ElementTree.XML(response)
    
    l = []
    for e in list(root):
        if e.tag == "Episode":
            season = 0
            episode = 0
            for info in list(e):
                if info.tag == "SeasonNumber":
                    season = int(info.text)
                if info.tag == "EpisodeNumber":
                    episode = int(info.text)
            l.append("%s.s%02de%02d" %(name, season, episode))

    return l
