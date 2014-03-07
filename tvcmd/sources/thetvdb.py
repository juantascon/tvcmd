import urllib.parse

import xml.parsers.expat

from .. import errors
from . import base
from ..lib import xmltodict

import logging
def log(): return logging.getLogger(__name__)

APIKEY = "FD9D34DB64F25A09"

class TheTVDB(base.Base):
    def get_shows(self, pattern):
        url = "http://thetvdb.com/api/GetSeries.php?seriesname=%s" % (urllib.parse.quote(pattern))
        
        try:
            xml_content = self._get_url(url)
            xml_content_dict = xmltodict.parse(xml_content)
            
            data = xml_content_dict["Data"]
            if not data: raise errors.SourceError("Invalid show: empty source response")
            
            shows = data["Series"]
            if (not isinstance(shows, list)): shows = [shows]
            
            return [{"id": s["seriesid"], "name": s["SeriesName"]} for s in shows]
        except xml.parsers.expat.ExpatError:
            raise errors.SourceError("Invalid show: unexpected source response")
        except:
            raise
            
    def get_episodes(self, show_id):
        url = "http://thetvdb.com/api/%s/series/%s/all/en.xml" % (APIKEY, show_id)
        
        try:
            xml_content = self._get_url(url)
            xml_content_dict = xmltodict.parse(xml_content)
            
            episodes = xml_content_dict["Data"]["Episode"]
            if (not isinstance(episodes, list)): episodes = [episodes]
            l = []
            for e in episodes:
                l.append({
                    "name": e["EpisodeName"],
                    "episode": int(e["EpisodeNumber"]),
                    "season": int(e["SeasonNumber"]),
                    "date": e["FirstAired"]
                })
            return l
        except xml_content.parsers.expat.ExpatError:
            raise errors.SourceError("Invalid show id: unexpected source response")
        except:
            raise
