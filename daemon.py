import os
import json
import time

from tsboundary import tsboundary
from velsession import VelSession
from resource import Resource
from reservation import Reservation

from settings import VELOCITY_IP, DAEMON_USER, DAEMON_PSWD, \
        VELOCITY_DIR, REFRESH_INTERVAL, RESOURCE_CATEGORY, PIPELINE_SITES

'''
 Collect schedule info.
'''
def schedule(output, start, end):    
    reservations = []
    lmod = 0
    for pl in PIPELINE_SITES:
        r_info = rsv.getResvInPeriod(pl, start, end)

        for r in r_info['reservations']:
            item = {'title': pl, 'id': r['id'], 'start': r['start'], \
                    'end': r['end']}
            reservations.append(item)
            if int(r['lastModified']) > lmod:
                lmod = int(r['lastModified'])
            
    fs = open(output, 'w+')
    jr = {'lastModified': lmod, 'reservations': reservations}
    json.dump(jr, fs)
    fs.flush()
    fs.close()
    return lmod
    
'''
 Calculate resource utilization.
'''
def utilization(output):
    utilization = {}
    for rc in RESOURCE_CATEGORY:
        pinfo = rsc.getPortsOfCategory(rc)
        total = pinfo['total']
        if total == 0:
            utilization[rc]
        else:
            lc = 0
            for p in pinfo['ports']:
                if p['isLocked']:
                    lc += 1
        
            u = lc / total
            utilization[rc] = u
    
    fu = open(output, 'w+')
    json.dump(utilization, fu)
    fu.flush()
#    fu.seek(0)
#    print(fu.read())
    fu.close    

'''
 Update task process.
'''
def task_process(output, task):
    task_process = {}
    ft = open(task, 'r')
    tasks = json.load(ft)
    
    task_process['planned'] = tasks['total']
    passed = 0
    failed = 0
    for order in tasks['orders']:
        blades = tasks['tasks'][order]['blades']
        for b in blades:
            model = b['model']
            for key in tasks['tasks'][order][model].keys():
                if tasks['tasks'][order][model][key] == 'PASS':
                    passed += 1
                elif tasks['tasks'][order][model][key] == 'FAIL':
                    failed += 1
                else:
                    pass
                
    task_process['passed'] = passed
    task_process['failed'] = failed
    task_process['completed'] = passed + failed
    fp = open(output, 'w+')
    json.dump(task_process, fp)
    fp.flush()
#    fp.seek(0)
#    print(fp.read())
    fp.close
    

if __name__ == "__main__":
    
    vs = VelSession(host=VELOCITY_IP, user=DAEMON_USER, pswd=DAEMON_PSWD)
    rsc = Resource(vs)
    rsv = Reservation(vs)
    
    f_schedule = os.path.join(os.path.dirname(VELOCITY_DIR), 'ctfm', \
                    'template', 'data', 'schedule.json')
    f_utilization = os.path.join(os.path.dirname(VELOCITY_DIR), 'ctfm', \
                    'template', 'data', 'utilization.json')
    f_task = os.path.join(os.path.dirname(VELOCITY_DIR), 'ctfm', \
                    'template', 'data', 'result.json')
    f_process = os.path.join(os.path.dirname(VELOCITY_DIR), 'ctfm', \
                    'template', 'data', 'task_process.json')

    st = int(tsboundary('SOM') * 1000)
    et = int(tsboundary('EOM') * 1000)    
    while True:
        schedule(f_schedule, st, et)
        utilization(f_utilization)
        task_process(f_process, f_task)
        
        time.sleep(REFRESH_INTERVAL)
        print('*****')
        print(time.ctime())
        print('*****')
