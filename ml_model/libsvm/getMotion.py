import calendar
import csv
from datetime import timedelta
from datetime import datetime
import math
import matplotlib.pyplot as plt
import operator
import os
import random
import shutil
import statistics
from svm import *
from svmutil import *
import sys
import time

file1 = "../module_data_foot"
file2 = "../module_data_shank"
path = '.'
outpath = '../'
models = ['model0', 'model1']
dt = 0.25
y_name = { "walking":0.0, "running":1.0, "stopping":2.0, "jumping":4.0, 'resting':3.0 }
y_name_rev = {0.0:'walking', 1.0:'running', 2.0:'stopping', 4.0:'jumping', 3.0:'resting'}
N = 100# must less than minimal of sample = 122

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

def getLastOutput(filename):
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

    if not output:
        return []
    data1 = output[len(output)-1]
    while(len(data1) < 20):
        output.pop()
        data1 = output[len(output)-1]
    return data1

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

if __name__ == '__main__':
    data1 = getLastOutput(file1)
    data2 = getLastOutput(file2)

    time1 = []
    time2 = []
    foot_shank_pair = []

    for i in range(len(data1)):
        time_tmp = getTime(data1[i])
        time1.append(time_tmp)
        foot_shank_pair.append(-1)

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

    past = 0
    times = 1
    for i in range(len(foot_shank)):
        if (foot_shank[i][0][:19] == foot_shank[past][0][:19]):
            times += 1
        else:
            for j in range(past, i):
                foot_shank[j][0] = str(foot_shank[j][0])+'.'+str(int((j-past)*100/times)).strip('.')
            past = i
            times = 1
        foot_shank[i][2] = float(foot_shank[i][2])
        foot_shank[i][3] = float(foot_shank[i][3])
        foot_shank[i][4] = float(foot_shank[i][4])
        foot_shank[i][5] = float(foot_shank[i][5])
        foot_shank[i][6] = float(foot_shank[i][6])
        foot_shank[i][7] = float(foot_shank[i][7])
        foot_shank[i][10] = float(foot_shank[i][10])
        foot_shank[i][11] = float(foot_shank[i][11])
        foot_shank[i][12] = float(foot_shank[i][12])
        foot_shank[i][13] = float(foot_shank[i][13])
        foot_shank[i][14] = float(foot_shank[i][14])
        foot_shank[i][15] = float(foot_shank[i][15])
        norm_a_f = get_norm(foot_shank[i][2], foot_shank[i][3], foot_shank[i][4])
        norm_g_f = get_norm(foot_shank[i][5], foot_shank[i][6], foot_shank[i][7])
        norm_a_s = get_norm(foot_shank[i][10], foot_shank[i][11], foot_shank[i][12])
        norm_g_s = get_norm(foot_shank[i][13], foot_shank[i][14], foot_shank[i][15])
        foot_shank[i].append(norm_a_f)
        foot_shank[i].append(norm_g_f)
        foot_shank[i].append(norm_a_s)
        foot_shank[i].append(norm_g_s)
    for j in range(past, i+1):
        foot_shank[j][0] = str(foot_shank[j][0])+'.'+str(int((j-past)*100/times)).strip('.')
    for i in range(len(foot_shank)):
        foot_shank[i][0] = datetime.strptime(foot_shank[i][0], "%Y-%m-%d %H:%M:%S.%f")


    pre_times = []
    with open(outpath, 'r') as f:
        reader = csv.reader(f)
        pre_result = list(reader)
        if len(pre_result) > 1 and pre_result[1]:
            pre_times = [datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S.%f') for item in pre_result[1:]]
            print(pre_times)

    length = 0
    file_len = 0
    output = []
    for i in range(1, len(foot_shank)):
        if (time1[i] - time1[i-1]).seconds > 2:
            length = i
            continue
        elif (time1[i] == time1[i-1]):
            continue
        if i - length >= 19 and not foot_shank[i-19][0] in pre_times:
            datas = foot_shank[i-19:i+1]
            output.append(datas)
            file_len += 1

    predict = []
    for out in output:
        test_x = get_feature(out)
        dic = {}
        for i in range(len(test_x)):
            dic[i] = float(test_x[i])
        test_y = []

        for model in models:
            m = svm_load_model(path+model)
            result, acc, vals = svm_predict([], [dic], m)
            test_y.append(y_name_rev[float(result[0])])
        predict.append([datetime.strftime(out[0][0], '%Y-%m-%d %H:%M:%S.%f'), test_y[0], test_y[1]])

    with open(outpath, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(predict)
