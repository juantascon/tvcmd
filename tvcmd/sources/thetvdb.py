import urllib.parse
import datetime

from .. import errors, cons
from . import base

#import zipfile, io
import xml.etree.cElementTree as ElementTree

import logging
def log(): return logging.getLogger(__name__)

class TheTVDB(base.Base):
    def _get_xml(self, url):
        response = self._get_url(url)
        
        try: return ElementTree.XML(response.decode("utf-8"))
        except Exception as ex: raise errors.ServerError("Unexpected thetvdb.com XML response (%s)"%(ex))
        
    def get_shows(self, pattern):
        url = "http://thetvdb.com/api/GetSeries.php?seriesname=%s" % (urllib.parse.quote(pattern))
        
        try: root = self._get_xml(url)
        except errors.ServerError as ex: raise errors.ServerError("Show not found (%s)"%(ex))
        
        l = []
        for data in list(root):
            if data.tag == "Series":
                    info = { "name": None, "id": None }
                    for s in list(data):
                        if s.tag.lower() == "seriesid":
                            info["id"] = s.text
                        elif s.tag.lower() == "seriesname":
                            info["name"] = s.text
                    if info["id"]: l.append(info)
        
        return l
        
    def get_episodes(self, show_id):
        url = "http://thetvdb.com/api/%s/series/%s/all/en.xml" % (cons.APIKEY, show_id)
        
        try: root = self._get_xml(url)
        except errors.ServerError as ex: raise errors.ServerError("Error getting episodes list (%s)"%(ex))
        
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
        
        #log().debug(l)
        #log().debug("\n")
        return l
