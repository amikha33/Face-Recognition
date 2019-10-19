# -*- coding: utf-8 -*-
"""lda.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jn4nwJmYzB0Bup_dsuH29Nb823nQSgOI
"""

# !unzip ATT.zip
import cv2
import os
import glob
import numpy as np
import pandas as pd

img_dir = "./ATT"  # Enter Directory of all images
data_path = os.path.join(img_dir, '*g')
files = glob.glob(data_path)
data = []
i = 0
for f1 in files:
    i = i+1
    img = cv2.imread(f1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data.append(gray)
    mydata = np.array(data)
    # print("Image : \n",mydata)
# fixing shapev->400*10304
d = np.reshape(mydata, (400, 10304))
print("Shape od D matrix :", d.shape)

labels = []
personN=1
for i in range(1,401):

    person= str(personN)
    labels.append(person)
    z=i%10
    if z<1:
        # print("**IF**",personN)
        personN = personN +1

# print(labels)

data = pd.DataFrame(data=d)
data['labels'] = labels
data.iloc[[0]]

mu_all = [np.mean(data[col]) for col in data.columns[:-1]]
len(mu_all)

from numpy import linalg as LA 


labels = data.labels.unique()
mu = []  
l =0

#means
for i in labels:
    means=[]
    for col in data.columns[:-1]:
        means.append(np.mean(data[data['labels'] == i][col]))
    mu.append(means)
print(len(mu),len(mu[0]))

# b 
i =0
b = np.zeros((10304,10304))

for i in range(40):
    mat_diff = np.reshape(np.subtract(mu[i],mu_all),(10304,1))
    b = np.add(b,10*np.matmul(mat_diff,np.transpose(mat_diff)))
print(b.shape)
# print(np.transpose(matt_diff).shape)

#z[i]
z = []
for i in range(40):

    d = data[data['labels'] == labels[i]]
    d = d.drop('labels',axis=1)

    class_mean = np.reshape(mu[i],(10304,1))
    mean_by_ones_transpose =np.matmul(np.ones((10,1)),np.transpose(class_mean))
    z.append(np.subtract(d,mean_by_ones_transpose))

# print(data.shape)
# print('data shape',d.shape)
# print(mean_by_ones_transpose.shape)
# z = np.array(z)

#s[i]
S = np.zeros((10304,10304))
for i in range(40):
    mat = np.array(z[i])
    output = np.matmul(np.transpose(mat),mat)
    S = np.add(S,output)
print(S.shape)
# print(S)

#eigenvalues and eigenvectors
eigenvalues,eigenvectors = LA.eigh(np.matmul(LA.inv(S),b))
print(eigenvectors.shape)