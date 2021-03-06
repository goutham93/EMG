"""Plotting Live Data and Analysis of Data

use with arduino code "new3D"

features
- real-time plotting of up to 4 sensors
- automatic fuzzy c-means clustering
- lines between centroids
- continuous plotting with cluster predictions
"""


""" A. INITIALIZATION AND SETUP """


""" 1. importing relevant libraries """
import serial
import time
import datetime
import csv
import math
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import skfuzzy as fuzz

os.path.abspath("C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles")

""" 2. retrieving serial data """

# ser = serial.Serial(port = 'COM10', baudrate = 9600, timeout = None) #connected port
# print ("connected to: " + ser.portstr)

""" 3. number of sensors """

num_sensors = int(input("Number of sensors: "))
num_dim = int(input("Number of plotting dimensions: "))

""" 3. initializaing starting variables and functions"""

"""following function converts a 3D list to a 2D one"""
def threeDtotwoD(array): #array = 2D matrix (3 rows, N columns (number of samples))
    new_list = [[],[]]
    for i in range(len(array[0])):
        a = float(array[0][i])
        b = float(array[1][i])
        c = float(array[2][i])  
        f = (np.sqrt(3.0)/2)*(a-b)
        g = (1/2)*(2*c-a-b)
        r = np.sqrt(a**2 + b**2 + c**2)
        s = np.sqrt(f**2 + g**2 + 1)
        j = (r/s)*f
        k = (r/s)*g
        new_list[0].append(j)
        new_list[1].append(k)
    return new_list
        
"""following function converts a 3D list to another 3D one"""
def threeDconv(array): #array = 2D matrix (3 rows, N columns)
    new_list = [[],[],[]]
    for i in range(len(array[0])):
        a = float(array[0][i])
        b = float(array[1][i])
        c = float(array[2][i])  
        f = (np.sqrt(3.0)/2)*(a-b)
        g = (1/2)*(2*c-a-b)
        h = np.sqrt(a**2 + b**2 + c**2)
        s = np.sqrt(f**2 + g**2 + 1)
        x = (r/s)*f
        y = (r/s)*g
        new_list[0].append(x)
        new_list[1].append(y)
        new_list[2].append(h)
    return new_list

"""following function converts a 4D list into a 3D one"""
def fourDtothreeD(array): #array = 2D matrix (4 rows, N columns)
    new_list = [[],[],[]]
    for i in range(len(array[0])):
        a = float(array[0][i])
        b = float(array[1][i])
        c = float(array[2][i]) 
        d = float(array[3][i])
        x = a - (1/3)*(b+c+d)
        y = (np.sqrt(2)/3)*(2*b-c-d)
        z = (np.sqrt(2/3))*(c-d)
        new_list[0].append(x)
        new_list[1].append(y)
        new_list[2].append(z) 
    return new_list
    
line = []
index = 0
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']

if num_sensors == 2:
    all_data = [["logrms1","logrms2"]]
    fig0 = plt.figure(0)
elif num_sensors == 3:
    all_data = [["logrms1","logrms2", "logrms3"]]
    if num_dim == 3:
        fig0 = plt.figure(0)
        ax = plt.axes(projection = "3d")
    elif num_dim == 2:
        fig0 = plt.figure(0)
elif num_sensors == 4:
    all_data = [["logrms1","logrms2", "logrms3", "logrms4"]]
    fig0 = plt.figure(0)
    ax = plt.axes(projection = "3d")

start_time = time.time()
end_time = time.time()
all_data_proj3D = [[],[],[]]
all_data_proj2D = [[],[]]

""" B. INITIAL DATA COLLECTION AND ANALYSIS """

""" 1. data collection loop """

while end_time - start_time < 10:    #time in seconds
    a0 = str(np.random.randint(0,100))
    a1 = str(np.random.randint(0,100))
    a2 = str(np.random.randint(0,100))
    a3 = str(np.random.randint(0,100))
        
            
    if num_sensors == 2:
        a = [a0,a1]
        if ((len(a) == 2)):
            if (len(a[0])>=0 & len(a[1])>=0):
                x = float(a[0])
                y = float(a[1])
                all_data.append([x,y])
                plt.scatter(x,y,s=10, c = "y")
                plt.pause(0.00001)
    elif num_sensors == 3:
        a = [a0,a1,a2]
        if num_dim == 3:
            if ((len(a) == 3)):
                if (len(a[0])>=0 & len(a[1])>=0 & len(a[2])>=0):
                    x = float(a[0])
                    y = float(a[1])
                    z = float(a[2])
                    all_data.append([x,y,z])
                    ax.scatter(x,y,z, s=10, c = "y")
                    plt.pause(0.00001)
        elif num_dim == 2:
            
            if ((len(a) == 3)):
                if (len(a[0])>=0 & len(a[1])>=0 & len(a[2])>=0):
                    x = float(a[0])
                    y = float(a[1])
                    z = float(a[2])
                    all_data.append([x,y,z])
                    converted_xyz = threeDtotwoD([[x],[y],[z]])
                    all_data_proj2D[0].append(converted_xyz[0][0])
                    all_data_proj2D[1].append(converted_xyz[1][0])
                    j = converted_xyz[0][0]
                    k = converted_xyz[1][0]
                    plt.scatter(j,k,s=10, c = "y")
                    plt.pause(0.00001)
            
    elif num_sensors == 4:
        a = [a0,a1,a2,a3]
        if ((len(a) == 4)):
            if (len(a[0])>=0 & len(a[1])>=0 & len(a[2])>=0 & len(a[3])>=0):
                x = float(a[0])
                y = float(a[1])
                z = float(a[2])
                w = float(a[3])
                all_data.append([x,y,z,w])
                print(a)
                converted_xyzw = fourDtothreeD([[x],[y],[z],[w]])
                all_data_proj3D[0].append(converted_xyzw[0][0])
                all_data_proj3D[1].append(converted_xyzw[1][0])
                all_data_proj3D[2].append(converted_xyzw[2][0])
                j = converted_xyzw[0][0]
                k = converted_xyzw[1][0]
                l = converted_xyzw[2][0]
                ax.scatter(j,k,l,s = 10, c = "y")
                plt.pause(0.00001)
                
    index += 1
    end_time = time.time()
 
# """ 2. storing data in csv file """
# 
# num1 = datetime.datetime.now().date() 
# num2 = datetime.datetime.now().time() 
# num =  num1.isoformat() + "..." + num2.isoformat()
# num = (str(num).replace(":","-"))
# num = (str(num).replace("-","."))
# 
# with open('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\test' + num + '.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=' ',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for i in all_data:
#         writer.writerow(i)
# 
# print("file saved as: " + 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\test' + str(num) + '.csv')

""" 3. running the fuzzy c-means algorithm """

alldata = np.transpose(np.asarray(all_data[1:]))

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, 5, 2, error=0.0005, maxiter=10000, init=None, seed=None) #second par is clusters
cluster_membership = np.argmax(u, axis=0)

""" 4. plotting the points and centroids """

if num_sensors == 2:
    for j in range(5):      #change depending on number clusters
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                plt.scatter(alldata[0][i], alldata[1][i], color = colors[j], s= 20, marker = ".")
        plt.scatter(cntr[j][0], cntr[j][1], color = colors[j], s= 50, marker = "s")
elif (num_sensors == 3):
    if num_dim == 3:
        for j in range(5):
            for i in range(len(cluster_membership)):
                if cluster_membership[i] == j:
                    ax.scatter(alldata[0][i], alldata[1][i], alldata[2][i],c = colors[j], s = 50, marker = ".")
            ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
    elif num_dim == 2:
        cntr = np.transpose(np.array(threeDtotwoD(np.transpose(cntr))))
        for j in range(5):      #change depending on number clusters
            for i in range(len(cluster_membership)):
                if cluster_membership[i] == j:
                    plt.scatter(all_data_proj2D[0][i], all_data_proj2D[1][i], c = colors[j], s= 20, marker = ".")
            plt.scatter(cntr[j][0], cntr[j][1], color = colors[j], s= 50, marker = "s")

elif (num_sensors == 4):
    cntr = np.transpose(np.array(fourDtothreeD(np.transpose(cntr))))
    print(cntr)
    for j in range(5):
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                ax.scatter(all_data_proj3D[0][i], all_data_proj3D[1][i], all_data_proj3D[2][i],c = colors[j], s = 50, marker = ".")
        ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)    

""" 5. adding line between centroids """

if num_dim == 3:
    for point in cntr:
        for point2 in cntr:
            ax.plot([point[0], point2[0]], [point[1], point2[1]], [point[2], point2[2]],"-b")
if num_dim == 2:
    for point in cntr:
        for point2 in cntr:
            plt.plot([point[0], point2[0]], [point[1], point2[1]],"-b")
       
# """ 6. saving figure as a png file """
#     
# plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\fig' + num + '.png')
# print ("figure saved as: "+ 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\csvfiles\\fig' + num + '.png')

""" 7. resetting the plot with only centroids """

if num_dim == 2:
    fig1 = plt.figure(1)
if num_dim == 3:
    fig1 = plt.figure(1)
    ax = plt.axes(projection = "3d")

for j in range(5):              #change value to match clusters
    if num_dim == 2:
        plt.scatter(cntr[j][0], cntr[j][1], c = colors[j], marker = "s", s = 50)
    elif num_dim == 3:
        ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
        

""" C. CONTINUOUS REAL-TIME TRACKING """

# while True:    
#     a0 = str(np.random.randint(0,100))
#     a1 = str(np.random.randint(0,100))
#     a2 = str(np.random.randint(0,100))
#     a3 = str(np.random.randint(0,100))
# 
#     
#     if num_sensors == 2:
#         a = [a0,a1]
#         if ((len(a) == 2)):
#             if (len(a[0])>=4 & len(a[1])>=4):
#                 x = float(a[0])
#                 y = float(a[1])
# 
#                 a_array = np.asarray([[x], [y]])
#                 v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
#                 cluster_num = int(np.argmax(v[0], axis = 0))
#                 #print(a)
#                 plt.scatter(x,y, s=40, color = colors[cluster_num])
#                 plt.pause(0.000001)
#                 plt.clf()
#                 for j in range(5):    #change value to match clusters
#                     plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
#     elif num_sensors == 3:
#         a = [a0,a1,a2]
#         if num_dim == 3:
#             if ((len(a) == 3)):
#                 if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>=4):
#                     x = float(a[0])
#                     y = float(a[1])
#                     z = float(a[2])
#                     a_array = np.asarray([[x], [y], [z]])
#                     v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
#                     cluster_num = int(np.argmax(v[0], axis = 0))
#                     #print(a)
#                     ax.scatter(x,y,z, s=40, color = colors[cluster_num])
#                     plt.pause(0.00001)
#                     plt.clf()
#                     for j in range(5):    #change value to match clusters
#                         ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
#         
#         elif num_dim == 2:
#             if ((len(a) == 3)):
#                 if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>=4):
#                     x = float(a[0])
#                     y = float(a[1])
#                     z = float(a[2])
#                     a_array = np.asarray([[x], [y], [z]])
#                     v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
#                     cluster_num = int(np.argmax(v[0], axis = 0))
#                     converted_xyz = threeDtotwoD([[x],[y],[z]])
#                     j = converted_xyz[0][0]
#                     k = converted_xyz[1][0]
#                     plt.scatter(j,k,s=10, c = colors[cluster_num])
#                     plt.pause(0.00001)
#                     plt.clf()
#                     for j in range(5):    #change value to match clusters
#                         plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
#         
#     
#     elif num_sensors == 4:
#         a = [a0,a1,a2,a3]
#         if ((len(a) == 4)):
#             if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>=4 & len(a[3])>=4):
#                 x = float(a[0])
#                 y = float(a[1])
#                 z = float(a[2])
#                 w = float(a[3])
#                 a_array = np.asarray([[x], [y], [z],[w]])
#                 v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
#                 cluster_num = int(np.argmax(v[0], axis = 0))
#                 converted_xyzw = fourDtothreeD([[x],[y],[z],[w]])
#                 j = converted_xyz[0][0]
#                 k = converted_xyz[1][0]
#                 l = converted_xyz[2][0]
#                 ax.scatter(j,k,l,s = 10, c = colors[cluster_num])
#                 plt.pause(0.00001)
#                 plt.clf()
#                 for j in range(5):    #change value to match clusters
#                     ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
# #                         
# #                         
#         line = []

