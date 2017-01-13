import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # @UndefinedVariable

class VelSession():

    def __init__(self, host, user, pswd):
        
        self.base_url =     'https://' + host
        self.headers =      {'X-Auth-Token': '', 'Content-type': 'application/json'}
        
        auth_url = 'https://' + user + ':' + pswd + '@' + host + \
                   '/velocity/api/auth/v1/token'
        response = requests.get(auth_url, verify=False)
        
        if response.status_code == 200:
            rd = json.loads(response.text)
            self.headers['X-Auth-Token'] = rd['token']

    def get(self, url):
        r = requests.get(url, headers=self.headers, verify=False)
        return json.loads(r.text)

    def post(self, url, body):
        # Have to tranform dict to json string, then Velocity can parse successfully.
        jstr = json.dumps(body)
        r = requests.post(url, headers=self.headers, data=jstr, verify=False)
        if(len(r.text) > 0):
            return json.loads(r.text)


