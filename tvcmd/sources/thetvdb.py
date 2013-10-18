import urllib.parse
import datetime

import xml.parsers.expat

from .. import errors, cons
from . import base
from ..lib import xmltodict

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
        
        try:
            xml_content = self._get_url(url)
            xml_content_dict = xmltodict.parse(xml_content)
            xml_content_dict_shows = list(xml_content_dict["Data"].values())
            return [{ "id": s["seriesid"], "name": s["SeriesName"]} for s in xml_content_dict_shows]
        except xml.parsers.expat.ExpatError:
            raise errors.SourceError("Invalid show: unexpected source response")
        except:
            raise
            
    def get_episodes(self, show_id):
        url = "http://thetvdb.com/api/%s/series/%s/all/en.xml" % (cons.APIKEY, show_id)
        
        try:
            xml_content = self._get_url(url)
            xml_content_dict = xmltodict.parse(xml_content)
            
            l = []
            #print(xml_content_dict["Data"]["Episode"])
            for episode in xml_content_dict["Data"]["Episode"]:
                l.append({
                    "name": episode["EpisodeName"],
                    "episode": int(episode["EpisodeNumber"]),
                    "season": int(episode["SeasonNumber"]),
                    "date": self._isostr_to_date(episode["FirstAired"])
                })
            return l
        except xml_content.parsers.expat.ExpatError:
            raise errors.SourceError("Invalid show id: unexpected source response")
        except:
            raise
        