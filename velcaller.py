import json
from collections import OrderedDict
from velsession import VelSession

class VelCaller():

    vsession = None

    def __init__(self, vs):
        self.vsession = vs

    def vget(self, url, sort=False, **params):
        '''
        params can be:
            sortBy - sorted by specific key.
            filter - filtered by specific key.
            other API related parameters 
        '''
        if(self.vsession != None):
            if len(params) > 0:
                url = self.vsession.base_url + url + '?'
                for key in params:
                    if isinstance(params[key], list):
                        p = '&'.join(params[key])
                    else:
                        p = params[key]
                    url = url + key + '=' + p + '&' 
                url = url.rstrip('&') 
            else:
                url = self.vsession.base_url + url

            r = self.vsession.get(url).text
            if sort:
                return json.loads(r, object_pairs_hook=OrderedDict)
            else:
                return json.loads(r)
            
    def vpost(self, url, body=None, **params):
        if(self.vsession != None):
            if len(params) > 0:
                url = self.vsession.base_url + url + '?'
                for key in params:
                    url = url + key + '=' + params[key] + '&' 
                url = url.rstrip('&') 
            else:
                url = self.vsession.base_url + url            

            return self.vsession.post(url, body)
        
    def vtime(self):
        url = '/velocity/api/util/v1/time'
        return self.vget(url)
    
if __name__ == "__main__":
    vs = VelSession(host='192.168.1.21', user='jimmy', pswd='Spirent')
    vc = VelCaller(vs)
    print(vc.vtime())
