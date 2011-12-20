#! /usr/bin/env python

import httplib2
import xml.etree.cElementTree as ElementTree

APIKEY = "FD9D34DB64F25A09"

def _get_url(url):
    h = httplib2.Http(cache = "/tmp/tvcmd-cache")
    resp, content = h.request(url, "GET")
    str_content = content.decode("utf-8")
    return str_content

def get_show_id(show):
    url = "http://thetvdb.com/api/GetSeries.php?seriesname=%s" % (show)
    response = _get_url(url)
    root = ElementTree.XML(response)
    series = list(root)[0]
    
    for s in list(series):
        if s.tag == "seriesid":
            return s.text
    return None

def get_episode_info(show, season, episode):
    id = get_show_id(show)
    
    url = "http://thetvdb.com/api/%s/series/%s/default/%d/%d/en.xml" % (APIKEY, id, season, episode)
    response = _get_url(url)
    root = ElementTree.XML(response)
    
    info = {}
    for e in list(list(root)[0]):
        if e.tag == "FirstAired":
            info["firstaired"] = e.text
        if e.tag == "EpisodeName":
            info["episodename"] = e.text
    
    return info
    
def get_episodes_list(show):
    id = get_show_id(show)
    
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
            l.append("%s.s%02de%02d" %(show, season, episode))

    return l

if __name__ == "__main__":
    print(get_episode_info("lost", 1, 2))
    
