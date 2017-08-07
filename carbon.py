import socket
import time
import json
import pickle
import struct
import os
import subprocess
import whisper

CARBON_SERVER = '0.0.0.0'
CARBON_PORT = 2004

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

def workingMain(inJson):
    jFile = open(inJson)
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    for line in jFile.readlines():
        job = json.loads(line)
        print job['_id']
        dictions = build(job)
        for diction in dictions:
            message = []
            for point in range(len(diction['datapoints'])):
                path = str('JOBS.' + str(job['_id'])[:7] + '.' + str(diction['target']))
                value = diction['datapoints'][point][0]
                times = diction['datapoints'][point][1]
                #temp = (path, (times, value))
                temp = (path, (time.time() - point*30, value))
                message.append(temp)
            package = pickle.dumps(message, 1)
            size = struct.pack('!L', len(package))
            send = size + package
            sock.sendall(send)
    sock.close()

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
                print "error " + str(job['_id'])[:7] + '/' + str(diction['target'])
            for point in range(len(diction['datapoints'])):
                path = str('JOBS.' + str(job['_id'])[:7] + '.' + str(diction['target']))
                value = diction['datapoints'][point][0]
                times = diction['datapoints'][point][1]
                #temp = (path, (times, value))
                temp = (path, (time.time() - point*30, value))
                message.append(temp)
            package = pickle.dumps(message, 1)
            size = struct.pack('!L', len(package))
            send = size + package
            sock.sendall(send)
    sock.close()

mainPickle('timeseries-resource_1.json', '30s', '1d')
#workingMain('timeseries-resource_1.json')
