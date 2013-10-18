from .. import errors, cons

import httplib2
import logging
def log(): return logging.getLogger(__name__)

class Base:
    def _get_url(self, url):
        #log().debug("\nGETURL: %s\n"%(url))
        
        try:
            h = httplib2.Http(cache = cons.CACHEDIR)
            resp, content = h.request(url, "GET", headers={"cache-control":"private,max-age=86400"})
        except Exception as ex:
            raise ServerError("Error connecting to server: %s" % (ex))
        
        if (resp["status"] != "200"):
            raise ServerError("Invalid server response: %s" % (resp))
        
        return content
    
    def get_shows(self, pattern):
        return []
    
    def get_episodes(self, show_id):
        return []
        