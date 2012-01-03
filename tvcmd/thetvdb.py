import httplib2
import urllib.parse

#import zipfile, io
import xml.etree.cElementTree as ElementTree
import datetime

from tvcmd.errors import (ServerError)
from tvcmd import cons

import logging
def log(): return logging.getLogger(__name__)

def _get_url(url):
    # log().debug("\nGETURL: %s\n"%(url))
    
    try:
        h = httplib2.Http(cache = cons.CACHEDIR)
        resp, content = h.request(url, "GET", headers={"cache-control":"private,max-age=86400"})
    except: raise ServerError("Error connecting thetvdb.com")
    
    if (resp["status"] == "200"): return content
    else: raise ServerError("Invalid thetvdb.com response")

# def _get_xml_zip():
#     response = zipfile.ZipFile(io.BytesIO(_get_url(url))).read("en.xml")
#     return response
    
def _get_xml(url):
    response = _get_url(url)
    
    try: return ElementTree.XML(response.decode("utf-8"))
    except Exception as ex: raise ServerError("Unexpected thetvdb.com XML response (%s)"%(ex))

def get_show_info(show_name):
    shows = get_shows(show_name)
    
    try: return shows[0]
    except: raise ServerError("Show not found")
    
def get_shows(pattern):
    url = "http://thetvdb.com/api/GetSeries.php?seriesname=%s" % (urllib.parse.quote(pattern))
    
    try: root = _get_xml(url)
    except ServerError as ex: raise ServerError("Show not found (%s)"%(ex))
    
    l = []
    for data in list(root):
        if data.tag == "Series":
                info = { "name": None, "id": None, "language": None }
                for s in list(data):
                    if s.tag.lower() == "seriesid":
                        info["id"] = s.text
                    elif s.tag.lower() == "seriesname":
                        info["name"] = s.text
                    elif s.tag.lower() == "language":
                        info["language"] = s.text
                if info["id"]: l.append(info)
    
    return l
    
def get_episodes(show_id):
    url = "http://thetvdb.com/api/%s/series/%s/all/en.xml" % (cons.APIKEY, show_id)
    
    try: root = _get_xml(url)
    except ServerError as ex: raise ServerError("Error getting episodes list (%s)"%(ex))
    
    l = []
    for data in list(root):
        if data.tag.lower() == "episode":
            info = { "season": None, "episode": None, "name": "", "date": datetime.date.max }
            
            for e in list(data):
                if e.tag.lower() == "seasonnumber":
                    info["season"] = int(e.text)
                elif e.tag.lower() == "episodenumber":
                    info["episode"] = int(e.text)
                elif e.tag.lower() == "firstaired":
                    try: info["date"] = datetime.date(int(e.text[0:4]), int(e.text[5:7]), int(e.text[8:10]))
                    except: pass
                elif e.tag.lower() == "episodename":
                    info["name"] = e.text
                    
            l.append(info)
    
    return l

