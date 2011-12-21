#! /usr/bin/env python

import httplib2
import xml.etree.cElementTree as ElementTree
import datetime
import zipfile
import io
import logging

APIKEY = "FD9D34DB64F25A09"

def log():
    return logging.getLogger(__name__)

def _get_url(url):
    log().debug(url)
    h = httplib2.Http(cache = "/tmp/tvcmd-cache")
    resp, content = h.request(url, "GET", headers={"cache-control":"private,max-age=86400"})
    return content

def get_show_id(show):
    url = "http://thetvdb.com/api/GetSeries.php?seriesname=%s" % (show)
    response = _get_url(url).decode("utf-8")
    root = ElementTree.XML(response)
    series = list(root)[0]
    
    for s in list(series):
        if s.tag == "seriesid":
            return s.text
    return None

def get_episodes(show):
    id = get_show_id(show)
    
    url = "http://thetvdb.com/api/%s/series/%s/all/en.xml" % (APIKEY, id)
    # response = zipfile.ZipFile(io.BytesIO(_get_url(url))).read("en.xml")
    response = _get_url(url).decode("utf-8")
    root = ElementTree.XML(response)
    
    l = []
    for e in list(root):
        if e.tag == "Episode":
            d = { "show": show, "season": None, "episode": None, "name": "", "date": datetime.date.max }
            
            for info in list(e):
                if info.tag == "SeasonNumber":
                    d["season"] = int(info.text)
                elif info.tag == "EpisodeNumber":
                    d["episode"] = int(info.text)
                elif info.tag == "FirstAired":
                    try: d["date"] = datetime.date(int(info.text[0:4]), int(info.text[5:7]), int(info.text[8:10]))
                    except: pass
                elif info.tag == "EpisodeName":
                    d["name"] = info.text
                    
            l.append(d)
                
    return l
    
if __name__ == "__main__":
    get_episodes("lost")
