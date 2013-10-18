import urllib.parse
import datetime

import xml.parsers.expat

from .. import errors
from . import base
from ..lib import xmltodict

import logging
def log(): return logging.getLogger(__name__)

class TVRage(base.Base):
    def get_shows(self, pattern):
        url = "http://services.tvrage.com/feeds/search.php?show=%s" % (urllib.parse.quote(pattern))
        
        try:
            xml_content = self._get_url(url)
            xml_content_dict = xmltodict.parse(xml_content)
            xml_content_dict_shows = list(xml_content_dict["Results"].values())[0]
            
            return [{ "id": s["showid"], "name": s["name"]} for s in xml_content_dict_shows]
        except xml.parsers.expat.ExpatError:
            raise errors.SourceError("Invalid show: unexpected source response")
        except:
            raise
    
    def get_episodes(self, show_id):
        url = "http://services.tvrage.com/feeds/episode_list.php?sid=%s" % (show_id)
        
        try:
            xml_content = self._get_url(url)
            xml_content_dict = xmltodict.parse(xml_content)
        except xml_content.parsers.expat.ExpatError:
            raise errors.SourceError("Invalid show id: unexpected source response")
        except:
            raise
        
        l = []
        for season in xml_content_dict["Show"]["Episodelist"]["Season"]:
            for episode in season["episode"]:
                l.append({
                    "name": episode["title"],
                    "episode": int(episode["seasonnum"]),
                    "season": int(season["@no"]),
                    "date": self._isostr_to_date(episode["airdate"])
                })
        return l
        