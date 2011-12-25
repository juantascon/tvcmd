import httplib2
import xml.etree.cElementTree as ElementTree
import datetime
#import zipfile, io

from tvcmd.errors import (ServerError)

import logging
def log(): return logging.getLogger(__name__)

APIKEY = "FD9D34DB64F25A09"

def _get_url(url):
    # log().debug("GETURL: "+url)
    
    try:
        h = httplib2.Http(cache = "/tmp/tvcmd-cache")
        resp, content = h.request(url, "GET", headers={"cache-control":"private,max-age=86400"})
    except: raise ServerError("Error connecting thetvdb.com")
    
    if (resp["status"] == "200"): return content
    else: raise ServerError("Invalid thetvdb.com response")

def _get_xml_zip():
    # response = zipfile.ZipFile(io.BytesIO(_get_url(url))).read("en.xml")
    pass
    
def _get_xml(url):
    response = _get_url(url)
    
    try: return ElementTree.XML(response.decode("utf-8"))
    except: raise ServerError("Unexpected thetvdb.com response")

def get_show_info(show_name):
    url = "http://thetvdb.com/api/GetSeries.php?seriesname=%s" % (show_name)
    
    try: root = _get_xml(url)
    except ServerError as ex: raise ServerError("Show not found (%s)"%(ex))
    
    l = []
    for data in list(root):
        if data.tag == "Series":
                info = { "show": show_name, "name": None, "id": None, "language": None }
                for s in list(data):
                    if s.tag == "seriesid":
                        info["id"] = s.text
                    if s.tag == "SeriesName":
                        info["name"] = s.text
                    if s.tag == "language":
                        info["language"] = s.text
                if info["id"]: l.append(info)
    
    if len(l) > 0: return l
    else: raise ServerError("Show not found")

def get_episodes(show_name, show_id):
    url = "http://thetvdb.com/api/%s/series/%s/all/en.xml" % (APIKEY, show_id)
    
    try: root = _get_xml(url)
    except ServerError as ex: raise ServerError("Error getting episodes list (%s)"%(ex))
    
    l = []
    for e in list(root):
        if e.tag == "Episode":
            d = { "show": show_name, "season": None, "episode": None, "name": "", "date": datetime.date.max }
            
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

