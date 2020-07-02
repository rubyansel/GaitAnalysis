import os
from datetime import datetime
from datetime import timedelta
import time
import operator
import sys
import shutil
import csv
import math
import random

dt = 0.25
y_name = { "walking":0.0, "running":1.0, "stopping":2.0, "jumping":4.0, "resting":3.0 }
output_file = 'train'
test_file = 'test'
N = 100# must less than minimal of sample = 122

def getTime(data):
    time_obj = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
    return time_obj

def get_norm(a, b, c):
    return math.sqrt(a*a+b*b+c*c)

def is_heap(data, mid, col):
    if mid == 0 or mid == len(data)-1:
        return False
    if (data[mid-1][col] < data[mid][col] and data[mid][col] > data[mid-1][col]):
        return True
    else:
        return False

def getDelta(data):
    max_del = [ [0.0]*12,[10000000000.0]*12 ]
    for i in range(len(data)):
        max_del[0][0] = max(data[i][2], max_del[0][0])
        max_del[0][1] = max(data[i][3], max_del[0][1])
        max_del[0][2] = max(data[i][4], max_del[0][2])
        max_del[0][3] = max(data[i][5], max_del[0][3])
        max_del[0][4] = max(data[i][6], max_del[0][4])
        max_del[0][5] = max(data[i][7], max_del[0][5])
        max_del[0][6] = max(data[i][10], max_del[0][6])
        max_del[0][7] = max(data[i][11], max_del[0][7])
        max_del[0][8] = max(data[i][12], max_del[0][8])
        max_del[0][9] = max(data[i][13], max_del[0][9])
        max_del[0][10] = max(data[i][14], max_del[0][10])
        max_del[0][11] = max(data[i][15], max_del[0][11])

        max_del[1][0] = min(data[i][2], max_del[1][0])
        max_del[1][1] = min(data[i][3], max_del[1][1])
        max_del[1][2] = min(data[i][4], max_del[1][2])
        max_del[1][3] = min(data[i][5], max_del[1][3])
        max_del[1][4] = min(data[i][6], max_del[1][4])
        max_del[1][5] = min(data[i][7], max_del[1][5])
        max_del[1][6] = min(data[i][10], max_del[1][6])
        max_del[1][7] = min(data[i][11], max_del[1][7])
        max_del[1][8] = min(data[i][12], max_del[1][8])
        max_del[1][9] = min(data[i][13], max_del[1][9])
        max_del[1][10] = min(data[i][14], max_del[1][10])
        max_del[1][11] = min(data[i][15], max_del[1][11])
    delta = []
    for i in range(len(max_del[0])):
        delta.append(float(max_del[0][i] - max_del[1][i]))
    return delta

def getPeriod(data):
    period = [ [], [], [], [], [], [], [], [], [], [], [], [] ]
    for i in range(len(data)):
        if (is_heap(data, i, 2)):
            period[0].append(i)
        if (is_heap(data, i, 3)):
            period[1].append(i)
        if (is_heap(data, i, 4)):
            period[2].append(i)
        if (is_heap(data, i, 5)):
            period[3].append(i)
        if (is_heap(data, i, 6)):
            period[4].append(i)
        if (is_heap(data, i, 7)):
            period[5].append(i)

        if (is_heap(data, i, 10)):
            period[6].append(i)
        if (is_heap(data, i, 11)):
            period[7].append(i)
        if (is_heap(data, i, 12)):
            period[8].append(i)
        if (is_heap(data, i, 13)):
            period[9].append(i)
        if (is_heap(data, i, 14)):
            period[10].append(i)
        if (is_heap(data, i, 15)):
            period[11].append(i)
    for i in range(len(period)):
        first = data[period[i][0]]
        last = data[period[i][-1]]
        delta_time = (last[0] - first[0]).seconds + (last[0] - first[0]).microseconds / 1000000
        period[i] = delta_time / len(period[i])
    return period

def getMaxNorm(data):
    max_nor = [ 0.0 ]*4
    for i in range(len(data)):
        max_nor[0] = max(data[i][16], max_nor[0])
        max_nor[1] = max(data[i][17], max_nor[1])
        max_nor[2] = max(data[i][18], max_nor[2])
        max_nor[3] = max(data[i][19], max_nor[3])
    return max_nor

def getMinNorm(data):
    min_nor = [10000000000000000.0]*4
    for i in range(len(data)):
        min_nor[0] = min(data[i][16], min_nor[0])
        min_nor[1] = min(data[i][17], min_nor[1])
        min_nor[2] = min(data[i][18], min_nor[2])
        min_nor[3] = min(data[i][19], min_nor[3])
    return min_nor

def getPeriodNorm(data):
    period_norm = [ [], [], [], [] ]
    for i in range(len(data)):
        if (is_heap(data, i, 16)):
            period_norm[0].append(i)
        if (is_heap(data, i, 17)):
            period_norm[1].append(i)
        if (is_heap(data, i, 18)):
            period_norm[2].append(i)
        if (is_heap(data, i, 19)):
            period_norm[3].append(i)
    for i in range(len(period_norm)):
        first = data[period_norm[i][0]]
        last = data[period_norm[i][-1]]
        delta_time = (last[0] - first[0]).seconds + (last[0] - first[0]).microseconds / 1000000
        period_norm[i] = delta_time / len(period_norm[i])
    return period_norm
        

def get_feature(data):
    '''
    | time_f | name_f | ax_f | ay_f | az_f | gx_f | gy_f | gz_f |
    | time_s | name_s | ax_s | ay_s | az_s | gx_s | gy_s | gz_s |
    | norm_a_f | norm_g_f | norm_a_s | norm_g_s |
    '''
    past = 0
    times = 1
    for i in range(len(data)):
        if (data[i][0][:19] == data[past][0][:19]):
            times += 1
        else:
            for j in range(past, i):
                data[j][0] = str(data[j][0])+'.'+str(int((j-past)*100/times)).strip('.')
            past = i
            times = 1
        data[i][2] = float(data[i][2])
        data[i][3] = float(data[i][3])
        data[i][4] = float(data[i][4])
        data[i][5] = float(data[i][5])
        data[i][6] = float(data[i][6])
        data[i][7] = float(data[i][7])
        data[i][10] = float(data[i][10])
        data[i][11] = float(data[i][11])
        data[i][12] = float(data[i][12])
        data[i][13] = float(data[i][13])
        data[i][14] = float(data[i][14])
        data[i][15] = float(data[i][15])
        norm_a_f = get_norm(data[i][2], data[i][3], data[i][4])
        norm_g_f = get_norm(data[i][5], data[i][6], data[i][7])
        norm_a_s = get_norm(data[i][10], data[i][11], data[i][12])
        norm_g_s = get_norm(data[i][13], data[i][14], data[i][15])
        data[i].append(norm_a_f)
        data[i].append(norm_g_f)
        data[i].append(norm_a_s)
        data[i].append(norm_g_s)
    for j in range(past, i+1):
        data[j][0] = str(data[j][0])+'.'+str(int((j-past)*100/times)).strip('.')
    for i in range(len(data)):
        data[i][0] = datetime.strptime(data[i][0], "%Y-%m-%d %H:%M:%S.%f")

    output = []
    delta = getDelta(data)
    period = getPeriod(data)
    max_nor = getMaxNorm(data)
    min_nor = getMinNorm(data)
    period_norm = getPeriodNorm(data)
    output += [ delta[2], delta[3], delta[10], delta[11] ]
    #output += delta
    output += [max_nor[1]]
    output += [max_nor[3]]
    #output += max_nor
    #output += min_nor
    #output += period
    #output += period_norm
    return output

def preprocess2(motion, inputfile, outputfile):
    '''
    For data to process, we want to have
    | max_delax_f | max_delay_f | max_delaz_f | max_delgx_f | max_delgy_f | max_delgz_f |
      max_delax_s | max_delay_s | max_delaz_s | max_delgx_s | max_delgy_s | max_delgz_s |
      max_nor_a_f | max_nor_g_f | max_nor_a_s | max_nor_g_s |
      min_nor_a_f | min_nor_g_f | min_nor_a_s | min_nor_g_s |
      period_ax_f | period_ay_f | period_az_f | period_gx_f | period_gy_f | period_gz_f |
      period_ax_s | period_ay_s | period_az_s | period_gx_s | period_gy_s | period_gz_s |
      per_nor_a_f | per_nor_g_f | per_nor_a_s | per_nor_g_s |

    Actually we have
    | max_delaz_f | max_delgx_f | max_delgy_s | max_delgz_s | max_nor_g_f | max_nor_g_s |
    Output files like
     y  x_1  x_2  ... 
    in float

    y=0 for walking
    y=1 for running
    y=2 for jumping
    y=3 for stopping
    '''
    with open(inputfile, newline = '') as f:
        reader = csv.reader(f)
        data = list(reader)
    out_data = get_feature(data)
    output = [y_name[motion]]
    for data in out_data:
        output.append("{:e}".format(data))
    with open(outputfile, 'a', newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow(output)
    return

path = '.' # Absolute path

files = os.listdir(path)
dirpath = []
for dirfile in files:
    if dirfile.isdecimal():
        dirpath.append(dirfile)

dirname = ['walking', 'running', 'stopping', 'resting']
motionNum = [637, 122, 225, 500] # Alternate yourselves
''' Collect all raw data from directories
for direc in dirpath:
    for name in dirname:
        os.chdir(path+'/'+direc)
        files = os.listdir()
        if not name in files:
            continue
        print(direc+'/'+name)
        os.chdir(name)
        files = os.listdir()
        for fille in files:
            names = fille.split('_')
            shutil.copyfile(path+'/'+direc+'/'+name+'/'+fille, path+'/'+name+'/'+direc+'_'+names[-2]+'_'+names[-1])
            print(path+'/'+name+'/'+direc+'_'+names[-2]+'_'+names[-1])
    os.chdir(path)
colName = []
for i in range(37):
    colName.append(i)
'''
open(path+'/'+output_file, 'w').close()
'''
with open(path+'/'+output_file, 'a', newline='') as f:
    writer = csv.writer(f, delimiter=' ')
    writer.writerow(colName)
'''
open(path+'/'+test_file, 'w').close()
'''
with open(path+'/'+test_file, 'a', newline='') as f:
    writer = csv.writer(f, delimiter=' ')
    writer.writerow(colName)
'''
select = []
select_test = []
for name in dirname:
    select.append(random.sample(range(1, motionNum[int(y_name[name])]+1), N))
for name in dirname:
    select_test.append(random.sample(range(1, motionNum[int(y_name[name])]+1), 21))
    motionNum[int(y_name[name])] = 0

for direc in dirpath:
    for name in dirname:
        os.chdir(path+'/'+direc)
        files = os.listdir()
        if not name in files:
            continue
        print(direc+'/'+name)
        os.chdir(name)
        files = os.listdir()
        for fille in files:
            motionNum[int(y_name[name])] += 1
            names = fille.split('_')
            if motionNum[int(y_name[name])] in select_test[int(y_name[name])]:
                preprocess2(name, path+'/'+direc+'/'+name+'/'+fille, path+'/'+test_file)
            elif motionNum[int(y_name[name])] in select[int(y_name[name])]:
                preprocess2(name, path+'/'+direc+'/'+name+'/'+fille, path+'/'+output_file)
    os.chdir(path)

for name in dirname:
    print(name+' has %d files.' %(motionNum[int(y_name[name])]))
