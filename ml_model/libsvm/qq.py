#!/usr/bin/python
import os
from svm import *
from svmutil import *
import matplotlib.pyplot as plt
import math
import statistics

train_path = '../train'
test_path = '../test'
yes = 0.0
C = [ 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
D = [ 2, 3 ]
R = [ 0, 1 ]
G = [ 100, 10, 1, 0.1, 0.01 ]

train_file = open(train_path, 'r')
train_lines = train_file.readlines()
train_y = []
train_x = []
train_file.close()

for i in range(len(train_lines)):
    sepe = train_lines[i].strip(' \n\r').split(' ')
    sepe = [x for x in sepe if x != '']
    dic = {}
    digit = float(sepe[0])
    for i in range(len(sepe)-1):
        dic[i] = float(sepe[i+1])
    if digit == yes:
        isyes = 1
    else:
        isyes = -1
    train_y.append(digit)
    #train_y.append(isyes)
    train_x.append(dic)

test_file = open(test_path, 'r')
test_lines = test_file.readlines()
test_y = []
test_x = []
test_file.close()

for i in range(len(test_lines)):
    sepe = test_lines[i].strip(' \n\r').split(' ')
    sepe = [x for x in sepe if x != '']
    dic = {}
    digit = float(sepe[0])
    for i in range(len(sepe)-1):
        dic[i] = float(sepe[i+1])
    if digit == yes:
        isyes = 1
    else:
        isyes = -1
    test_y.append(digit)
    #test_y.append(isyes)
    test_x.append(dic)

fig_data_y = []
cmd = '-s 0 -c 0.0001 -t 0 -q'
m = svm_train(train_y, train_x, cmd) #polynomial kernel
svm_save_model('model0', m)
m = svm_load_model('model0')
svm_predict(train_y, train_x, m)
cmd = '-s 0 -c 0.01 -t 1 -d 3 -g 0.1 -r 0 -q'
m = svm_train(train_y, train_x, cmd) #polynomial kernel
svm_save_model('model1', m)
'''
for c in C:
    #cmd = '-s 0 -c '+str(c)+' -t 1 -d '+str(d)+' -g '+str(g)+' -r '+str(r)+' -q'
    cmd = '-s 0 -c '+str(c)+' -t 0 -q'
    #cmd = '-s 0 -c '+str(c)+' -t 2  -g '+str(g)+' -q'
    #cmd = '-s 0 -c '+str(c)+' -t 3  -g '+str(g)+' -r '+str(r)+' -q'
    m = svm_train(train_y, train_x, cmd) #polynomial kernel
    #print('type 1, d %d, g %2f, r %d, C %.5f' %(d, g, r, c))
    print('type 0, C %.5f' %(c))
    #print('type 2, g %2f, C %.5f' %(g, c))
    #print('type 3, g %2f, r %d, C %.5f' %(g, r, c))
    print('train result')
    result, acc, vals = svm_predict(train_y, train_x, m)
    print(acc)
    print('test result')
    result, acc, vals = svm_predict(test_y, test_x, m)
    print(acc)
for d in D:
    for g in G:
        for r in R:
            for c in C:
                cmd = '-s 0 -c '+str(c)+' -t 1 -d '+str(d)+' -g '+str(g)+' -r '+str(r)+' -q'
                #cmd = '-s 0 -c '+str(c)+' -t 0 -q'
                #cmd = '-s 0 -c '+str(c)+' -t 2  -g '+str(g)+' -q'
                #cmd = '-s 0 -c '+str(c)+' -t 3  -g '+str(g)+' -r '+str(r)+' -q'
                m = svm_train(train_y, train_x, cmd) #polynomial kernel
                print('type 1, d %d, g %2f, r %d, C %.5f' %(d, g, r, c))
                #print('type 0, C %.5f' %(c))
                #print('type 2, g %2f, C %.5f' %(g, c))
                #print('type 3, g %2f, r %d, C %.5f' %(g, r, c))
                print('train result')
                result, acc, vals = svm_predict(train_y, train_x, m)
                print(acc)
                print('test result')
                result, acc, vals = svm_predict(test_y, test_x, m)
                print(acc)
for g in G:
    for c in C:
        #cmd = '-s 0 -c '+str(c)+' -t 1 -d '+str(d)+' -g '+str(g)+' -r '+str(r)+' -q'
        #cmd = '-s 0 -c '+str(c)+' -t 0 -q'
        cmd = '-s 0 -c '+str(c)+' -t 2  -g '+str(g)+' -q'
        #cmd = '-s 0 -c '+str(c)+' -t 3  -g '+str(g)+' -r '+str(r)+' -q'
        m = svm_train(train_y, train_x, cmd) #polynomial kernel
        #print('type 1, d %d, g %2f, r %d, C %.5f' %(d, g, r, c))
        #print('type 0, C %.5f' %(c))
        print('type 2, g %2f, C %.5f' %(g, c))
        #print('type 3, g %2f, r %d, C %.5f' %(g, r, c))
        print('train result')
        result, acc, vals = svm_predict(train_y, train_x, m)
        print(acc)
        print('test result')
        result, acc, vals = svm_predict(test_y, test_x, m)
        print(acc)
for g in G:
    for r in R:
        for c in C:
            #cmd = '-s 0 -c '+str(c)+' -t 1 -d '+str(d)+' -g '+str(g)+' -r '+str(r)+' -q'
            #cmd = '-s 0 -c '+str(c)+' -t 0 -q'
            #cmd = '-s 0 -c '+str(c)+' -t 2  -g '+str(g)+' -q'
            cmd = '-s 0 -c '+str(c)+' -t 3  -g '+str(g)+' -r '+str(r)+' -q'
            m = svm_train(train_y, train_x, cmd) #polynomial kernel
            #print('type 1, d %d, g %2f, r %d, C %.5f' %(d, g, r, c))
            #print('type 0, C %.5f' %(c))
            #print('type 2, g %2f, C %.5f' %(g, c))
            print('type 3, g %2f, r %d, C %.5f' %(g, r, c))
            print('train result')
            result, acc, vals = svm_predict(train_y, train_x, m)
            print(acc)
            print('test result')
            result, acc, vals = svm_predict(test_y, test_x, m)
            print(acc)
'''
