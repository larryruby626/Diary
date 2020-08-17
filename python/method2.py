
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
#        self.A = np.fromfile('C:\\Users\1\2007006\\Desktop\\HS_TemporalNoise.raw', dtype='int16', sep="")
        #==============raw input================        
        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2.raw', dtype='int16', sep="")
        #==============get the numb of pictures ================
        self.raw_length = int((np.size(self.A))/1779456) 
        #==============(reshape to N*1779456*1)================
        B = np.reshape(self.A,(self.raw_length,1779456))
        
        #==============(reshape to cell size - N*1324(high)*1344(width))================
        self.arr=np.zeros((self.raw_length,1324,1344))
        for i in range(self.raw_length):
            pic1 =  B[i][:]
            pic1arr = np.reshape(pic1,(1324,1344))
            self.arr[i][:][:] = pic1arr
     #==============(取得列平均值)================           
    def avgrow(self):
        self.avvgg=[]
        pic_1 = self.arr[0]
        for i  in range(1324):
            newx = pic_1[i,:]
            avg_row = np.mean(newx) 
            self.avvgg.append(avg_row)
        return self.avvgg
    #==============(取得列平均值)================           
    def get_median(self,numofpic):
        self.md=[]
        pic_1=copy.deepcopy(self.arr[numofpic]) # use deep copy to avoid the origin array changed
        for i  in range(1324):
            newx = pic_1[i,:]
            avg_row = np.median(newx) 
            self.md.append(avg_row)
        return self.md
    
    
    def de_gate_noise_v1(self,x,numofpic):
        
        avg_row =x
        avg_all = np.mean(avg_row)
        avg_row = (avg_row-avg_all)*(-1)
        pic=copy.deepcopy(self.arr[numofpic]) # use deep copy to avoid the origin array changed
        out_arr =[]
        for i in range(1324):
            pic[i,:] = pic[i,:]+avg_row[i]
            for j in range(1344):
                out_arr.append((pic[i,j]))   
        return out_arr
    
    def de_gate_noise_v2(self,x,numofpic):
        avg_row =x
        avg_all = np.mean(avg_row)
        avg_row = (avg_row-avg_all)*(-1)
        pic=copy.deepcopy(self.arr[numofpic]) # use deep copy to avoid the origin array changed
#        out_arr =[]
        for i in range(1324):
            pic[i,:] = pic[i,:]+avg_row[i]
        return pic  
    
    def de_data_noise(self,after_degate_noise):
        data_medi = []
        arr = after_degate_noise
        for i in range(42):
            adr1 = 0+(32*i)
            adr2 = 32+(32*i)
            data_medi.append(np.median(arr[:,adr1:adr2]))
        sum_d_m = sum(data_medi)/42
        data_medi = (data_medi - sum_d_m)*(-1)
        for i in range(42):
            adr1 = 0+(32*i)
            adr2 = 32+(32*i)
            arr[:,adr1:adr2]=arr[:,adr1:adr2]+data_medi[i]
        return  arr
    #==============(data reshape to one line array)================ 
    def arr_to_row(self,arr):
        out_arr =[]        
        for i in range(1324):
            for j in range(1344):
                out_arr.append((arr[i,j]))   
        return out_arr        
    
    def de_gate_noise_allpic(self):
        all_pic=np.array([])
        for i in range(self.raw_length):
#            pic=copy.deepcopy(self.arr[i]) # use deep copy to avoid the origin array changed
            avg_row =self.get_median(i)
            xx = self.de_gate_noise_v1(avg_row,i)
            xx = np.array(xx)
            all_pic =np.hstack([all_pic,xx])
        return all_pic

    # 將 1 row nparray save as int16 raw file
    def saveto_raw(self,out_arr,filename):
        out_arr = np.asarray(out_arr, dtype=np.int16)
        path = 'C:\\Users\\2007006\\Desktop\\'+ filename+'.raw'
        out_arr.astype('int16').tofile(path)
    
    #mutiple_pic 有去除雜訊功能
    def smoothy(self,count):
        x= self.get_median(count)
        y=self.de_gate_noise_v2(x,count)
        z=copy.deepcopy(self.de_data_noise(y))
        #------ Z 底完datanoise
        mid = np.median(z)
        aa= (z-mid)*0.95
        z = z - aa
        K = A.arr_to_row(z)
        return K

#===========col-direction denoise============
    def de_colway(self,x,minusV):
        avvgg=[]
        pic_1=copy.deepcopy(x) # use deep copy to avoid the origin array changed
        for i  in range(1344):
            newx = pic_1[:,i]
            avg_row = np.median(newx) 
            avvgg.append(avg_row)
            for j in range(1324):
                pic_1[j,i] =pic_1[j,i]-avvgg[i]
        x = x -(pic_1*minusV)
        return x 
#===========row-direction denoise============
    def de_rowway(self,x,minusV):  
        avvgg=[]
        pic_1=copy.deepcopy(x) # use deep copy to avoid the origin array changed
        for i  in range(1324):
            newx = pic_1[i,:]
            avg_row = np.median(newx) 
            avvgg.append(avg_row)
            for j in range(1344):
                pic_1[i,j] =pic_1[i,j]-avvgg[i]
        x = x -(pic_1*minusV)
        return x     
    def method0713_delcol(self,i):
        
        x = self.arr[i]
        y = self.de_colway(x,0.8)   #do method2(gate denoise)1 times
        y1 = self.de_colway(y,0.8)  #do method2(gate denoise)2 times
        z =A.de_data_noise(y1)    #do method2(data denoise)
        K = A.arr_to_row(z) 
        return K

if __name__ == '__main__':
    time_start=time.time()
# ========================== method2 ========================
    A = xray()
    narry = np.array([])
    for i in range(A.raw_length):
#    for i in range(1):           #if you jsut run one frame
        K = A.method0713_delcol(i)
        narry =np.append(narry,K)
        
    A.saveto_raw(narry,'method2_1time_30')   # save one-line array to raw file
    

    time_end=time.time()
    process_time =np.round((time_end-time_start),2)
    print(process_time)
# =============================================================================



    
    
