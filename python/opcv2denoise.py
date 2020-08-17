# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:57:49 2020

@author: 2007006
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt


def draw_on_plot(pos, src, title):
    plt.subplot(pos), plt.imshow(src), plt.title(title)
    plt.xticks([]), plt.yticks([])
    
def read_arr(arr,numb):
    temp =arr[0+numb*1779456:1779456+numb*1779456]
    arr = np.reshape(temp,(1324,1344))
    return arr

def arr_to_row(self,arr): 
    out_arr =[]        
    for i in range(3072):
        for j in range(3072):
            out_arr.append((arr[i,j]))   
    return out_arr  
    
#save the one line data to file

def saveto_raw(arr,filename):
    out_arr =[]        
    for i in range(1324):
        for j in range(1344):
            out_arr.append((arr[i,j]))   
        
    out_arr = np.asarray(out_arr, dtype=np.int16)
    path = 'C:\\Users\\2007006\\Desktop\\'+ filename+'.raw'
    out_arr.astype('int16').tofile(path)
    
    
A = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2.raw', dtype='int16', sep="")
img = read_arr(A,0)
#img = cv2.imread('data/opencv-logo-white.png')

draw_on_plot(241, img, 'Original')

kernel = np.ones((3, 3), np.float32)/9
dst = cv2.filter2D(img, -1,kernel)
draw_on_plot(242, dst, 'Averaging 3x3')
saveto_raw(dst,'Averaging 3x3')

kernel = np.ones((5, 5), np.float32)/25
dst = cv2.filter2D(img, -1, kernel)
draw_on_plot(243, dst, 'Averaging 5x5')
saveto_raw(dst,'Averaging 5x5')


kernel = np.ones((7, 7), np.float32)/25
dst = cv2.filter2D(img, -1, kernel)
draw_on_plot(244, dst, 'Averaging 7x7')
saveto_raw(dst,'Averaging 7x7')


blur = cv2.blur(img, (5, 5))
draw_on_plot(245, blur, 'Blurred')
saveto_raw(blur,'Blurred')


gaussian_blur = cv2.GaussianBlur(img, (5, 5), 0)
draw_on_plot(246, gaussian_blur, 'Gaussian Blurred')
saveto_raw(gaussian_blur,'Gaussian Blurred')


median_blur = cv2.medianBlur(img, 5)
draw_on_plot(247, gaussian_blur, 'Median Blurred')
saveto_raw(median_blur,'Median Blurred')


bilateral_filter = cv2.bilateralFilter(img, 9, 75, 75)
draw_on_plot(248, bilateral_filter, 'Bilateral Filter')
saveto_raw(bilateral_filter,'Bilateral Filter')

plt.show()