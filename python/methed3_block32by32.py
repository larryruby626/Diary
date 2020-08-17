# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:38:07 2020

@author: 2007006
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 08:00:21 2020

@author: 2007006
"""
import sys
import numpy as np
import cv2
from matplotlib import pylab as plt
from matplotlib import pyplot
import copy
import time
class xray():
    
    def __init__(self):
#        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\HS_TemporalNoise.raw', dtype='int16', sep="")
        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2_6processdata\\raw2.raw', dtype='int16', sep="")
        
        #==============(get the pic_length of pic)================           
        self.raw_length = int((np.size(self.A))/1779456)
        
        #==============(reshape one line data to pic_length*1779456)================
        B = np.reshape(self.A,(self.raw_length,1779456))
        self.arr=np.zeros((self.raw_length,1324,1344))
        
        #==============( save pic_length*1779456 to pic_length*13324*1344 )================
        for i in range(self.raw_length):
            pic =  B[i][:]
            picarr = np.reshape(pic,(1324,1344))
            self.arr[i][:][:] = picarr
            
    #==============( # 1280*1280 translate to one line  )================
    def arr_to_row(self,arr):  
        out_arr =[]        
        for i in range(1324):
            for j in range(1344):
                out_arr.append((arr[i,j]))   
        return out_arr  
        
    #==============(  #save the one line data to file  )================
    def saveto_raw(self,out_arr,filename): 
        out_arr = np.asarray(out_arr, dtype=np.int16)
        path = 'C:\\Users\\2007006\\Desktop\\'+ filename+'.raw'
        out_arr.astype('int16').tofile(path)
    
if __name__ == '__main__':
    time_start=time.time()
    A = xray()
    narry = np.array([])
    ALL_median = np.median(A.arr)
    std =np.std(A.arr[:])  # ALL frame std
    mean_arr=np.zeros((A.raw_length,42,42))


#    for u in range(A.raw_length):
    for u in range(1):
        pic1=copy.deepcopy(A.arr[u]) # use deep copy to avoid the origin array changed
        for i  in range(42):
            x1 = 0+32*i
            x2= 32+32*i
            for j in range(42):
                if j<=40:       #因為1324/32不能整除所以最後一個 block 以32*12處理 
                    y1=0+32*j
                    y2=32+32*j
                else:
                    y1=0+32*j
                    y2=12+32*j
#----------------use every block of mean to substract themself -------------
                temp_mean1 = np.mean(pic1[y1:y2,x1:x2])
                pic1[y1:y2,x1:x2] = pic1[y1:y2,x1:x2] - temp_mean1
#------------------- gate direction denoise--------------------                
                aaa =pic1[y1:y2,x1:x2]               
                for z in range(32):
                    if j>=41 and z>=12:# when deal the block size of 12*32 do nothing
                        continue
                    temp_mean = np.median(aaa[z,np.where(pic1[y1+z,x1:x2]<std*3)])
                    pic1[y1+z,x1:x2] -= temp_mean        
                    
        pic1 = pic1 + ALL_median # picture do offset
        K = A.arr_to_row(pic1)
        narry =np.append(narry,K)
    
    A.saveto_raw(narry,'outfilename') 
    
    time_end=time.time()
    process_time =np.round((time_end-time_start),2)
    print(process_time)