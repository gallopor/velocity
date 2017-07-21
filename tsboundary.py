import time
import datetime
import calendar

'''
 Timestamp of period boundary.
 tsb = NOW SOD EOD SOW EOW SOM EOM
'''
def tsboundary(tsb='NOW'):
    today = datetime.date.today()
    ds = datetime.time.min
    de = datetime.time.max
    penum = {
        'SOD': datetime.datetime.combine(today, ds),
        'EOD': datetime.datetime.combine(today, de),
        'SOW': datetime.datetime.combine(today - \
                    datetime.timedelta(today.weekday() + 1), ds),     
        'EOW': datetime.datetime.combine(today + \
                    datetime.timedelta(6 - today.weekday() - 1), de),
        'SOM': datetime.datetime.combine(datetime.date(today.year, today.month, \
                    1), ds),     
        'EOM': datetime.datetime.combine(datetime.date(today.year, today.month, \
                    calendar.monthrange(today.year, today.month)[1]), de),
    }
    if tsb == 'NOW':
        ts = time.time()
    else:
        ts = time.mktime(penum[tsb].timetuple())
    return ts


if __name__ == "__main__":
    
    for tsb in ['NOW', 'SOD', 'EOD', 'SOW', 'EOW', 'SOM', 'EOM']:
        ts = tsboundary(tsb)
        print(ts)
    
    
