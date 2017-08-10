import socket
import time
import json
import pickle
import struct
import os
import subprocess
import whisper
import sys
from getopt import getopt

CARBON_SERVER = '0.0.0.0'
CARBON_PORT = 2004

def usage():
    print " -f             specify the source json file. You must specify the file."
    print " -t             choose the interval time for data points and "
    print "                amount of time to be stored in the format "
    print "                interval:amount, 's' for seconds, 'h' for hours, "
    print "                and 'd' for days. I.e. 30s:5d for 5 days of 30 second intervals"
    print "                (default is 30s:7d)."
    print " -s             specify the server ip that carbon-cache is using"
    print "                (default server is 0.0.0.0)."
    print " -p             choose which port carbon-cache is running on"
    print "                (default port is 2004)."
    print " -h             display this help message and exit."

# This function takes in all of a job's data and outputs it as a list of dictionaries
# [{target : metricName, datapoints : [[datapoint, time], [datapoint, time], ...]}, ...]
def build(job):
    out = []
    keys = job.keys()
    keys.remove('_id')
    keys.remove('version')
    keys.remove('hosts')
    offset = 0
    for target in keys:
        canGo = True
        try:
            times = job[target]['times']
        except:
            # This filters out metrics in a job that don't have any data
            canGo = False
            print 'Error in ' + job['_id'][:7] + ' ' + target
        if canGo:
            for z in range(0, len(job[target]['hosts'])):
                diction = {'target': str(target) + str(z), 'datapoints':[]}
                out.append(diction)
                values = job[target]['hosts'][str(z)]['all']
                for x in range(0, len(times)):
                    out[z+offset]['datapoints'].append([values[x], int(times[x])])
            offset += len(job[target]['hosts'])
    return out

def timeToSeconds(inTime):
    switch = inTime[-1:]
    if switch == 's':
        return int(inTime[:len(inTime)-1])
    if switch.isdigit():
        return int(inTime)
    elif switch == 'h':
        return 60 * 60 * int(inTime[:len(inTime)-1])
    elif switch == 'd':
        return 60 * 60 * 24 * int(inTime[:len(inTime)-1])
    else:
        print 'invalid time format'
        return 0

# This method handles creating the files for whisper and population of the files
def mainPickle(inJson, inter, timeS):
    jFile = open(inJson)
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    for line in jFile.readlines():
        job = json.loads(line)
        print job['_id']
        dictions = build(job)
        if not os.path.exists('/opt/graphite/storage/whisper/JOBS/' + str(job['_id'])[:7]):
            os.makedirs('/opt/graphite/storage/whisper/JOBS/' + str(job['_id'])[:7])
        for diction in dictions:
            message = []
            try:
                interval = timeToSeconds(inter)
                timeSpan = timeToSeconds(timeS)
                whisper.create('/opt/graphite/storage/whisper/JOBS/' + str(job['_id'])[:7] + '/' + str(diction['target']) + '.wsp', [(interval, timeSpan/interval)], 0.5, 'average', 'store_true', 'store_true')
            except:
                # This catches exceptions and ignores exceptions thrown by whisper for attempting to create files that already exist
                exc_type, exc_value, exc_traceback = sys.exc_info()
                if str(exc_value)[-15:] != 'already exists!':
                    print('Unexpected error: ' + str(exc_value))

            for point in range(len(diction['datapoints'])):
                path = str('JOBS.' + str(job['_id'])[:7] + '.' + str(diction['target']))
                value = diction['datapoints'][point][0]
                times = diction['datapoints'][point][1]
                temp = (path, (times, value))
                message.append(temp)
            package = pickle.dumps(message, 1)
            size = struct.pack('!L', len(package))
            send = size + package
            sock.sendall(send)
    sock.close()

def main():
    opts, _ = getopt(sys.argv[1:], "p:s:t:f:h")

    f = ''
    i = '30s'
    t = '7d'

    for opt in opts:
        if opt[0] == '-p':
            CARBON_PORT = opt[1]

        if opt[0] == '-s':
            CARBON_SERVER = opt[1]

        if opt[0] == '-t':
            middle = opt[1].find(':')
            i = opt[1][:middle]
            t = opt[1][middle + 1:]

        if opt[0] == '-f':
            f = opt[1]

        if opt[0] == '-h':
            usage()
            sys.exit(0)

    if f != '':
        mainPickle(f, i, t)
    else:
        print('You must provide a json file\n')
        usage()

if __name__ == "__main__":
    main()
