import time
from velsession import VelSession
from velcaller import VelCaller

class Reservation(VelCaller):
    '''
    Using singel reservation object, you can make multiple reservations.
    But I suggect to create multiple reservation objects to do this. 
    Because the reservation object has kept the last reservation info.
    You can make your code more clearly and more efficently.
    '''
    def __init__(self, vs):
        super(Reservation, self).__init__(vs)
        
        '''In the future, maybe can load the restful api from a json file'''
        self.restful_api_urls['get'].update({
            'topologies': '/velocity/api/topology/v4/topologies',
            'reservations': '/velocity/api/reservation/v5/reservations',
            'reservation': '/velocity/api/reservation/v5/reservation/${reservation_id}',
        })
        self.restful_api_urls['post'].update({
            'reservation': '/velocity/api/reservation/v5/reservation',
            'reservation_action': \
                '/velocity/api/reservation/v5/reservation/${reservation_id}/action?type=${action}'
        })
           
        ''' 'description' can not be None. I don't know why?'''
        self.reservation_body = {
            'name': None,
            'description': '',
            'start': None,
            'end': None,
            'duration': None,
            'topologyId': None,
            'topologyVersionId': None,
            'cloudId': None,
            'isRecurrent': None,
            'recurrence': None,
            'resources': None,
            'intervalToRunEndTestCase': None,
            'startTestCases': None,
            'endTestCases': None,
            'request': None,
            'notes': None,
            'attendees': None,
            'resolution': None,
            'customConditions': None,
            'customUtilizations': None,
            'customLinkConditions': None,
            'workOrder': None
        } 
        
        self.last_reservation = None

    def topoReserve(self, name, duration):
        '''
        reservation's name is topology's name plus current time stamp.
        '''
        tp_f = 'name::' + name
        tp_info = self.vget('topologies', filter=tp_f)
        tp_id = tp_info['topologies'][0]['id']
     
        ts = time.strftime("%Y%m%d%H%M%S")
        resv_name = name + '-' + ts
        self.reservation_body['name'] = resv_name
        self.reservation_body['duration'] = duration
        self.reservation_body['topologyId'] = tp_id
        
        resv_info = self.vpost('reservation', self.reservation_body)
        self.last_reservation = resv_info
        return resv_info

    def topoRelease(self, resv_id=None):
        if(resv_id == None):
            if (self.last_reservation != None):
                resv_id = self.last_reservation['id']
        subst = {'reservation_id': resv_id, 'action': 'cancel'}

        return self.vpost('reservation_action', subst=subst)
           
    def resvQuery(self, resv_id=None, vfilter=None):
        if(resv_id != None):
            subst = {'reservation_id': resv_id}
            return resv.vget('reservation', subst=subst)
        if(vfilter != None):
#            params = 'filter=' + vfilter
            return resv.vget('reservations', vfilter=vfilter)
        return self.last_reservation
        
        
    def getActResvByTopo(self, tp_name):
        tp_f = 'filter=name::' + tp_name
        tp_info = self.vget('topologies', vfilter=tp_f)
        tp_id = tp_info['topologies'][0]['id']
        print(tp_id)
        resv_f = 'filter=status::ACTIVE' + '&' + 'filter=topologyId::' + tp_id
        return self.vget('reservations', vfilter=resv_f)
    
        
if __name__ == "__main__":
    vs = VelSession(host='192.168.1.11', user='jimmy', pswd='Spirent')
    resv = Reservation(vs)

#    resv_info = resv.topoReserve(name='ResourcesNoLink', duration=600)
#    print(resv_info)
    
#    time.sleep(5)
    
    resv_info = resv.getActResvByTopo('ResourcesNoLink')
    print(resv_info)
#    resv.topoRelease()

    
# url = Template(velocity_restful_url['topo_detail'])
# url = base_url.substitute(host=host) + url.substitute(reservation_id=resv_id)
# r = requests.get(url, headers=headers, verify=False)
# print(r.text)
# 
# url = base_url.substitute(host=host) + '/ito/executions/v1/executions'
# r = requests.get(url, headers=headers, verify=False)
# print(r.text)
