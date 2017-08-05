from velocity.velsession import VelSession
from velocity.velcaller import VelCaller

class Execution(VelCaller):

    def __init__(self, vs):
        super(Execution, self).__init__(vs)

        self.execution_body = {
            'callbackURL': None,
            'testPath': None,
            'parametersList': []
        } 
        
    def testExec(self, tpath, **params):
        url = '/ito/executions/v1/executions'
        self.execution_body['testPath'] = tpath
        self.execution_body['parametersList'] = params['parametersList']
        self.execution_body['callbackURL'] = params['callbackURL']
        tinfo = self.vpost(url, self.execution_body)
        return tinfo

    def testAbort(self, exec_id):
        pass
        
    def getExecsInfo(self, **params):
        '''
        params can be:
            offset - 
            limit - 
            filter - filtered by specific key.
        '''
        url = '/ito/executions/v1/executions/'
        return self.vget(url, params)
    
    def getSingleExecInfo(self, exec_id):
        url = '/ito/executions/v1/executions/' + exec_id
        return self.vget(url)
    
    def getTestReport(self, rep_id):
        url = '/ito/reporting/v1/reports/' + rep_id
        return self.vget(url)
    
    def getChildTestReports(self, parent_rep_id):
        url = '/ito/reporting/v1/reports/'
        rf = 'parentReport::' + parent_rep_id
        return self.vget(url, filter=rf)
        
if __name__ == "__main__":
    import time
    from velocity.settings import VELOCITY_IP, PIPELINE_SCRIPTS, PIPELINE_PARAMS
    
    vs = VelSession(host=VELOCITY_IP, user='jimmy', pswd='Spirent')
    ex = Execution(vs)
    
    topo = 'STCvPair'
    callbackURL = 'http://192.168.1.8:80/ctfm/notification'
    slot2 = 20000001
    slot7 = 20000002
    
    script = PIPELINE_SCRIPTS[topo]
    params = PIPELINE_PARAMS[topo]

    params = {'parametersList': [
        {'name': 'SlotPairs', 'value': '2:7'}, 
        {'name': 'SlotsCode', 'parameters': [
            {'name': 'Slot2', 'value': '10000001'},
            {'name': 'Slot7', 'value': '10000002'}
        ]}
    ]}
    ex_info = ex.testExec(script, parametersList=params['parametersList'])
    tid = ex_info['executionId']
    print(tid)
    #===========================================================================
    # time.sleep(20)
    # 
    # rst = ex.getSingleExecInfo(tid)
    # print(rst)
    # 
    # rep = ex.getTestReport(tid)
    # print(rep)
    # 
    # reps = ex.getChildTestReports(tid)
    # print(reps)
    #===========================================================================