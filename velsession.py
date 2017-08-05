import json
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class VelSession():

    def __init__(self, host, **params):
        
        self.base_url = 'https://' + host
        self.headers = {'X-Auth-Token': '', 'Content-type': 'application/json'}
        
        if 'token' in params:
            self.headers['X-Auth-Token'] = params['token']
        else:
            auth_url = 'https://' + params['user'] + ':' + params['pswd'] + '@' + host +\
                       '/velocity/api/auth/v1/token'
            response = requests.get(auth_url, verify=False)
        
            if response.status_code == 200:
                rd = json.loads(response.text)
                self.headers['X-Auth-Token'] = rd['token']

    def get(self, url):
        return requests.get(url, headers=self.headers, verify=False)

    def post(self, url, body):
        # Have to tranform dict to json string, then Velocity can parse successfully.
        jstr = json.dumps(body)
        r = requests.post(url, headers=self.headers, data=jstr, verify=False)
        if(len(r.text) > 0):
            return json.loads(r.text)
        
    def token(self):
        return self.headers['X-Auth-Token']

if __name__ == "__main__":
    vs1 = VelSession('10.23.155.231', user='demo', pswd='Spirent')
    token = vs1.token()
    print(token)
    
    #===========================================================================
    # vs2 = VelSession(host='192.168.1.21', token=token)
    # url = vs2.base_url + '/velocity/api/util/v1/time'
    # r = vs2.get(url).text
    # print(r)
    #===========================================================================
    
    #===========================================================================
    # jbody = '{"testPath": "CTM.itar/test_cases/R835E/SuiteR835E.fftc", "parametersList": [{"name": "SlotPairs", "value": "2:7"}, {"name": "SlotsCode", "parameters": [{"name": "Slot2", "value": "10000001"}, {"name": "Slot7", "value": "10000002"}]}]}' 
    # url = vs1.base_url + '/ito/executions/v1/executions'
    # r = requests.post(url, headers=vs1.headers, data=jbody, verify=False)
    # print(r.text)
    #===========================================================================

    execution_body = {
        'testPath': 'CTM.itar/test_cases/R835E/SuiteR835E.fftc',
        'parametersList': []
    } 

    params = {'parametersList': [
        {'name': 'SlotPairs', 'value': '2:7'}, 
        {'name': 'SlotsCode', 'parameters': [
            {'name': 'Slot2', 'value': '10000001'},
            {'name': 'Slot7', 'value': '10000002'}
        ]}
    ]}
    
    execution_body['parametersList'] = params['parametersList']
    url = vs1.base_url + '/ito/executions/v1/executions'
    r = vs1.post(url, execution_body)
    print(r)



