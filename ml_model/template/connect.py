import csv
from datetime import datetime
from datetime import timedelta
import time
import calendar
import operator
import sys
import os

#filename = sys.argv[1]
directory = sys.argv[1]
os.chdir(directory)
filename = 'module_data_'
file1 = 'module_data_foot_'
file2 = 'module_data_shank_'

def getTime(data):
    time_obj = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
    return time_obj

def print_file(data, start, motion, num, file_len):
    filename_adj = './'+motion+'/'+filename+motion+'_'+num+'_'+str(file_len).zfill(4)
    print('Writing '+filename_adj)
    f = open(filename_adj, 'w')
    w = csv.writer(f)
    for j in range(20):
        w.writerow(data[j+start])
    f.close()

files = os.listdir()
valid_foot_files = []
valid_shank_files = []
for dirfile in files:
    if dirfile.find(file1) == 0:
        valid_foot_files.append(dirfile)
    elif dirfile.find(file2) == 0:
        valid_shank_files.append(dirfile)

valid_foot_files.sort()
valid_shank_files.sort()


if not operator.eq(len(valid_foot_files), len(valid_shank_files)):
    sys.exit()
for n in range(len(valid_foot_files)):
    name = valid_foot_files[n].split('_')
    motion = name[-2]
    num = name[-1]
    time1 = []
    time2 = []
    foot_shank_pair = []

    with open(valid_foot_files[n], newline='') as f:
        reader = csv.reader(f)
        data1 = list(reader)
        data1 = data1[1:]
        for i in range(len(data1)):
            time_tmp = getTime(data1[i])
            time1.append(time_tmp)
            foot_shank_pair.append(-1)

    with open(valid_shank_files[n], newline='') as f:
        reader = csv.reader(f)
        data2 = list(reader)
        data2 = data2[1:]
        for i in range(len(data2)):
            time_tmp = getTime(data2[i])
            time2.append(time_tmp)

    for i in range(len(foot_shank_pair)):
        try:
            index = time2.index(time1[i])
        except ValueError:
            continue
        foot_shank_pair[i] = index
        time2[index] = 0

    for i in range(len(foot_shank_pair)):
        delta = timedelta(seconds = 1)
        if not operator.eq(foot_shank_pair[i], -1):
            continue
        try:
            index = time2.index(time1[i]+delta)
        except ValueError:
            continue
        foot_shank_pair[i] = index
        time2[index] = 0

    for i in range(len(foot_shank_pair)):
        delta = timedelta(seconds = 1)
        if not operator.eq(foot_shank_pair[i], -1):
            continue
        try:
            index = time2.index(time1[i]-delta)
        except ValueError:
            continue
        foot_shank_pair[i] = index
        time2[index] = 0

    foot_shank = []
    time1.clear()
    for i in range(len(foot_shank_pair)):
        if operator.eq(foot_shank_pair[i], -1):
            continue
        tmp_list = data1[i] + data2[foot_shank_pair[i]]
        foot_shank.append(tmp_list)
        time_tmp = getTime(data1[i])
        time1.append(time_tmp)

    length = 0
    file_len = 0
    for i in range(1, len(foot_shank)):
        if (time1[i] - time1[i-1]).seconds > 2:
            length = i
            continue
        elif (time1[i] == time1[i-1]):
            continue
        if i - length >= 19:
            print_file(foot_shank, i-19, motion, num, file_len)
            file_len += 1

    filename_adj = filename+motion+'_'+num
    print('Writing '+filename_adj)
    f = open(filename_adj, 'w')
    w = csv.writer(f)
    w.writerow(['time_foot','name_foot','ax_foot','ay_foot','az_foot','gx_foot','gy_foot','gz_foot','time_shank','name_shank','ax_shank','ay_shank','az_shank','gx_shank','gy_shank','gz_shank'])
    for j in range(len(foot_shank)):
        w.writerow(foot_shank[j])
    f.close()
