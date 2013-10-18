from .. import errors, cons

import httplib2
import datetime

import logging
def log(): return logging.getLogger(__name__)

class Base:
    def _isostr_to_date(self, _str):
        try:
            return datetime.date(int(_str[0:4]), int(_str[5:7]), int(_str[8:10]))
        except:
            return datetime.date.max
        
    def _get_url(self, url):
        #log().debug("\nGETURL: %s\n"%(url))
        h = httplib2.Http(cache = cons.CACHEDIR)
        resp, content = h.request(url, "GET", headers={"cache-control":"private,max-age=86400"})
        return content
    
    def get_shows(self, pattern):
        return []
    
    def get_episodes(self, show_id):
        return []
        