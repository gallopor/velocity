import json
from string import Template
from velsession import VelSession

class VelCaller():

    vsession = None

    def __init__(self, vs):
        self.vsession = vs
        self.restful_api_urls = {
            'get':      {'time': '/velocity/api/util/v1/time'},
            'post':     dict(),
            'put':      dict(),
            'delete':   dict()
        }    

    def vget(self, key, pattern='json', **params):
        if(self.vsession != None):
            if len(params) > 0:
                if 'url' in params:
                    url = self.vsession.base_url + params['url']
                else:
                    url = self.vsession.base_url + self.restful_api_urls['get'][key]
                if 'subst' in params:
                    # The type of 'subst' is dict
                    url = Template(url).substitute(params['subst'])
                if 'vfilter' in params:
                    url = url + '?' + params['vfilter']   
            else:
                url = self.vsession.base_url + self.restful_api_urls['get'][key]
            
            r = self.vsession.get(url).text
            if(pattern == 'json'):
                r = json.loads(r)
            
            return r
            
    def vpost(self, key, body=None, **params):
        if(self.vsession != None):
            if len(params) > 0:
                if 'url' in params:
                    url = self.vsession.base_url + params['url']
                else:
                    url = self.vsession.base_url + self.restful_api_urls['post'][key]
                if 'subst' in params:
                    url = Template(url).substitute(params['subst'])
            else:
                url = self.vsession.base_url + self.restful_api_urls['post'][key]            

            return self.vsession.post(url, body)
        
    def vtime(self):
        return self.vget('time')
    
if __name__ == "__main__":
    vs = VelSession(host='192.168.1.11', user='jimmy', pswd='Spirent')
    vc = VelCaller(vs)
    print(vc.vtime())
