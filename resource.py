from velcaller import VelCaller

class Resource(VelCaller):
    def __init__(self, vs):
        super(Resource, self).__init__(vs)
    
    def getTempIdByName(self, name):
        tf = 'name::' + name
        url = '/velocity/api/inventory/v5/templates/'
        t_info = self.vget(url, filter=tf)
        t_id = t_info['templates'][0]['id']
        return t_id
        
    def getPortsOfCategory(self, cat):
        t_id = self.getTempIdByName(cat)
        
        url = '/velocity/api/inventory/v5/devices/ports/'
        pf = 'templateId::' + t_id
        return self.vget(url, filter=pf)
    
        
if __name__ == "__main__":
    from velsession import VelSession

#    vs = VelSession(host='192.168.1.21', user='daemon', pswd='Spirent')
    vs = VelSession(host='10.23.155.231', user='jimmy', pswd='Spirent')
    res = Resource(vs)
    
    p = res.getPortsOfCategory('STC')
    print(p)
