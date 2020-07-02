import csv
from datetime import datetime
import time
import calendar
import operator
import sys

filename = sys.argv[1]

def getTime(data):
    time_obj = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
    return time_obj

def getAvgData(data, start, end):
    ax = 0.0
    ay = 0.0
    az = 0.0
    gx = 0.0
    gy = 0.0
    gz = 0.0
    for i in range(start, end):
        ax += float(data[i][2])
        ay += float(data[i][3])
        az += float(data[i][4])
        gx += float(data[i][5])
        gy += float(data[i][6])
        gz += float(data[i][7])
    ax = ax / (start-end)
    ay = ay / (start-end)
    az = az / (start-end)
    gx = gx / (start-end)
    gy = gy / (start-end)
    gz = gz / (start-end)
    return ax, ay, az, gx, gy, gz

output = []
output_title = []

with open(filename, newline='') as csvfile:

    rows = csv.reader( (line.replace('\0', '') for line in csvfile) )
    data = list(rows)
    data = data[1:]

time_obj_pre = datetime.now()
ax_avg = 0.0
ay_avg = 0.0
az_avg = 0.0
gx_avg = 0.0
gy_avg = 0.0
gz_avg = 0.0
start = False
session_cnt = 0
for i in range(len(data)):
    if ((operator.eq(data[i][1], 'walking') or operator.eq(data[i][1], 'running') or operator.eq(data[i][1], 'jumping') or operator.eq(data[i][1], 'stopping') or operator.eq(data[i][1], 'resting')) and
        operator.eq(data[i][2], '0') and
        operator.eq(data[i][3], '0') and
        operator.eq(data[i][4], '0') and
        operator.eq(data[i][5], '0') and
        operator.eq(data[i][6], '0') and
        operator.eq(data[i][7], '0')):
        #print('Start new session')
        ax_avg, ay_avg, az_avg, gx_avg, gy_avg, gz_avg = getAvgData(data, i-10, i)
        start = True
        session_cnt += 1
        new_list = []
        output.append(new_list)
        output_title.append(data[i][1])
        continue

    if (i > 0 and (getTime(data[i]) - getTime(data[i-1])).seconds > 10):
        #print((getTime(data[i]) - getTime(data[i-1])).seconds)
        #print('End session')
        start = False

    if (start):
        for j in range(8):
            if (operator.eq(data[i][j], '')):
                data[i][j] = 0
        data[i][2] = round(float(data[i][2]) - ax_avg, 3)
        data[i][3] = round(float(data[i][3]) - ay_avg, 3)
        data[i][4] = round(float(data[i][4]) - az_avg, 3)
        data[i][5] = round(float(data[i][5]) - gx_avg, 3)
        data[i][6] = round(float(data[i][6]) - gy_avg, 3)
        data[i][7] = round(float(data[i][7]) - gz_avg, 3)
        output[session_cnt-1].append(data[i])

for i in range(len(output)):
    filename_adj = filename+'_'+output_title[i]+'_'+str(i).zfill(2)
    f = open(filename_adj, 'w')
    w = csv.writer(f)
    w.writerow(['time','name','ax','ay','az','gx','gy','gz'])
    for j in range(len(output[i])):
        w.writerow(output[i][j])
    f.close()
