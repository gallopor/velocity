import time
from velocity.velcaller import VelCaller

class Reservation(VelCaller):
    '''
    Using singel reservation object, you can make multiple reservations.
    But I suggect to create multiple reservation objects to do this. 
    Because the reservation object has kept the last reservation info.
    You can make your code more clearly and more efficently.
    '''
    def __init__(self, vs):
        super(Reservation, self).__init__(vs)
        
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

    def getTopoIdByName(self, name):    
        url = '/velocity/api/topology/v4/topologies'
        tp_f = 'name::' + name
        tp_info = self.vget(url, filter=tp_f)
        tp_id = tp_info['topologies'][0]['id']
        return tp_id
 
    def topoReserve(self, name, duration):
        '''
        reservation's name is topology's name plus current time stamp.
        '''
        tp_id = self.getTopoIdByName(name)
        ts = time.strftime("%Y%m%d%H%M%S")
        resv_name = name + '-' + ts
        self.reservation_body['name'] = resv_name
        self.reservation_body['duration'] = duration
        self.reservation_body['topologyId'] = tp_id
        
        url = '/velocity/api/reservation/v5/reservation'
        resv_info = self.vpost(url, self.reservation_body)
        self.last_reservation = resv_info
        return resv_info

    def topoRelease(self, resv_id=None):
        if(resv_id == None):
            if (self.last_reservation != None):
                resv_id = self.last_reservation['id']
        url = '/velocity/api/reservation/v5/reservation/' + \
                resv_id + '/action?type=cancel'
        return self.vpost(url)
           
    def getActResvByTopo(self, tp_name):
        tp_id = self.getTopoIdByName(tp_name)
        
        url = '/velocity/api/reservation/v6/reservations/' 
        vfilter = ['status::ACTIVE', 'topologyId::' + tp_id]
        return self.vget(url, filter=vfilter)
    
    def getActResvByMe(self):
        user = self.vget('/velocity/api/user/v6/profile/current')
        user_id = user['id']
    
        url = '/velocity/api/reservation/v6/reservations/' 
        vfilter = ['status::ACTIVE', 'creatorId ::' + user_id]
        return self.vget(url, filter=vfilter)
    
    def getResvInPeriod(self, tp_name, start, end):
        tp_id = self.getTopoIdByName(tp_name)
        dp = {
            'filter': 'topologyId::' + tp_id, 
            'startAfter': str(start), 
            'endBefore': str(end), 
            'sortBy': 'created'
        }
        url = '/velocity/api/reservation/v6/reservations/' 
        return self.vget(url, **dp)
        
if __name__ == "__main__":
    from velocity.velsession import VelSession

    vs = VelSession(host='192.168.1.21', user='daemon', pswd='Spirent')
    resv = Reservation(vs)

