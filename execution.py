import time
from velsession import VelSession
from velcaller import VelCaller

class Execution(VelCaller):

    def __init__(self, vs):
        super(Execution, self).__init__(vs)
        
        '''In the future, maybe can load the restful api from a json file'''
        self.restful_api_urls['get'].update({
            'executions': '/ito/executions/v1/executions',
            'execution': '/ito/executions/v1/executions/${execution_id}',
            'report': '/ito/reporting/v0/reports/${report_id}/files/report.html'
        })
        self.restful_api_urls['post'].update({
            'execution': '/ito/executions/v1/executions',
        })
           
        self.execution_body = {
            'testPath': None
        } 
        
    def testExec(self, tpath):
        self.execution_body['testPath'] = tpath
        return self.vpost('execution', self.execution_body)

    def testAbort(self, exec_id):
        pass
        
    def getExecInfo(self, exec_id):
        subst = {'execution_id': exec_id}
        return self.vget('execution', subst=subst)
    
    def getTestReport(self, exec_id):
        ei = self.getExecInfo(exec_id)
        rep_id =  ei['reportID']
        print(rep_id)
        subst = {'report_id': rep_id}
        return self.vget('report', 'raw', subst=subst)
        
if __name__ == "__main__":
    vs = VelSession(host='192.168.1.11', user='jimmy', pswd='Spirent')
    ex = Execution(vs)

    tinfo = ex.testExec('CTM.itar/test_cases/R835E/SuiteR835E.fftc')
    print(tinfo)

    tid = tinfo['executionID']
    print(tid)
    
    time.sleep(5)
    
    rst = ex.getExecInfo(tid)
    print(rst)
    time.sleep(20)
    rep = ex.getTestReport(tid)
    print(rep)