"""
Velocity settings.

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

VELOCITY_DIR = os.path.dirname(os.path.abspath(__file__))

VELOCITY_IP = '192.168.1.21'
#VELOCITY_IP = '10.23.155.231'
DAEMON_USER = 'daemon'
DAEMON_PSWD = 'Spirent'
REFRESH_INTERVAL = 60

PIPELINE_SITES = ['STCvPair', 'SITE2']
PIPELINE_SCRIPTS = {
    'STCvPair': 'CTM.itar/test_cases/R835E/SuiteR835E.fftc',
    'SITE1': 'CTM.itar/test_cases/R835E/SuiteR835E.fftc',
    'SITE2': 'CTM.itar/test_cases/R835E/SuiteR835E.fftc'
}
PIPELINE_PARAMS = {
    'STCvPair': [
        {'name': 'SlotPairs', 'value': '2:7'}, 
        {'name': 'SlotsCode', 'parameters': [
            {'name': 'Slot2', 'value': '10000001'},
            {'name': 'Slot7', 'value': '10000002'}
        ]}
    ],
    'SITE1': [
        {'name': 'SlotPairs', 'value': '2:7'}, 
        {'name': 'SlotsCode', 'parameters': [
            {'name': 'Slot2', 'value': '10000001'},
            {'name': 'Slot7', 'value': '10000002'}
        ]}
    ],
    'SITE2': [
        {'name': 'SlotPairs', 'value': '2:7'}, 
        {'name': 'SlotsCode', 'parameters': [
            {'name': 'Slot2', 'value': '10000001'},
            {'name': 'Slot7', 'value': '10000002'}
        ]}
    ]
}
EXECUTION_QUEUE = {
    'STCvPair': [
        {'TC1': 'Slot2'},
        {'TC1': 'Slot7'},
        {'TC2': ['Slot2', 'Slot7']}
    ],
}
#NOTIFICATION_URL = 'http://10.39.183.240:80/ctfm/notification/'
#NOTIFICATION_URL = 'http://10.23.155.223:80/ctfm/notification/'
NOTIFICATION_URL = 'http://192.168.1.8:80/ctfm/notification/'
#NOTIFICATION_URL = 'http://10.23.155.251:80/ctfm/notification/'
RESOURCE_CATEGORY = ['STC']

if __name__ == "__main__":
    print(VELOCITY_DIR)