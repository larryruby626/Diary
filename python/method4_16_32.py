# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 08:44:22 2020

@author: 2007006
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 08:00:21 2020

@author: 2007006
"""
import numpy as np
import copy
import time
import cv2
class xray():
    
    def __init__(self):
#        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\HS_TemporalNoise.raw', dtype='int16', sep="")
        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2.raw', dtype='int16', sep="")
        # get the pic_length of pic 
        self.raw_length = int((np.size(self.A))/1779456)
        # reshape one line data to pic_length*1779456
        B = np.reshape(self.A,(self.raw_length,1779456))
        
        self.arr=np.zeros((self.raw_length,1324,1344))
        # save pic_length*1779456 to pic_length*13324*1344 
        for i in range(self.raw_length):
            pic =  B[i][:]
            picarr = np.reshape(pic,(1324,1344))
            self.arr[i][:][:] = picarr
            
    # 1280*1280 translate to one line 
    def arr_to_row(self,arr): 
        out_arr =[]        
        for i in range(1324):
            for j in range(1344):
                out_arr.append((arr[i,j]))   
        return out_arr  
        
    #save the one line data to file
    def saveto_raw(self,out_arr,filename): 
        out_arr = np.asarray(out_arr, dtype=np.int16)
        path = 'C:\\Users\\2007006\\Desktop\\'+ filename+'.raw'
        out_arr.astype('int16').tofile(path)
    def get_std(self,array):
        arr = array
        arr_std = np.std(arr[:,:])
        return  arr_std
#----------do process by 32*1 size--------------
    def newway32(self,array,std):
        pic1 =array
        ALL_median = np.median(self.arr)
        pic_minus = pic1-ALL_median    
        mean_arraa=np.zeros((1324,42))
    
        for i in range(42):
            for j in range(1324):
                y1=0+32*i
                y2=32+32*i  
                temp_x  = np.median(pic_minus[j,y1:y2]) # get the local median of the 32*1 block
                mean =list()
                for k in range(32):
                    temp_dev = pic_minus[j,(y1+k)]-temp_x  # minus local median
                    if abs(temp_dev)<3*std :               # (if > 3*std )==> defect point
                        mean.append(pic_minus[j,(y1+k)])   # 將符合<3*std  save to list 
                    else: 
                        pass
                mean_arraa[j,i] = np.mean(mean)
                
        pic2 = copy.deepcopy(pic1)
        for i  in range(42):
            for j  in range(1324):
                y1=0+32*i
                y2=32+32*i 
                pic2[j,y1:y2] -= mean_arraa[j,i]   #減去mean of list 
        
        return pic2
#----------do process by 16*1 size--------------
    def newway16(self,array,std):
        pic1  =array
        ALL_median = np.median(self.arr)
        pic_minus = pic1-ALL_median    
        mean_arraa=np.zeros((1324,84))
    
        for i in range(84):
            for j in range(1324):
                y1=0+16*i
                y2=16+16*i  
                temp_x  = np.median(pic_minus[j,y1:y2]) # the medain of the 1*16
                mean =list()
                for k in range(16):
                    temp_dev = pic_minus[j,(y1+k)]-temp_x 
                    if abs(temp_dev)<3*std  :              #avoid defect
                        mean.append(pic_minus[j,(y1+k)])
                    else: 
                        pass
                mean_arraa[j,i] = np.mean(mean)
                
        pic2 = copy.deepcopy(pic1)
        for i  in range(84):
            for j  in range(1324):
                y1=0+16*i
                y2=16+16*i  
                pic2[j,y1:y2] -= mean_arraa[j,i]   
        
        return pic2   
    


if __name__ == '__main__':
    time_start=time.time()

    A = xray()
    narry = []
    ALL_median = np.median(A.arr)
#-------------kerne------------      
    mx = np.array([[1,2,1],
                  [2,4,2],
                  [1,2,1]])
    
    pic2=np.zeros((1324,1344))
    medianx = np.median(A.arr[:])
        

    for i in range(A.raw_length):
#    for i in range(1):
        # get std of the current frame
        sstd = A.get_std(A.arr[i])  
        # get the processed of the current frame
#        pic2 = A.newway32(A.arr[i],sstd) 
        pic2 = A.arr[i] 
#        result = cv2.GaussianBlur(pic2,(3,3),0.5)
#        median = cv2.medianBlur(pic2, 5)
        K = A.arr_to_row(pic2)
        narry += K
    
    A.saveto_raw(narry,'filename')
    
    # clear variable
    del K,narry,pic2 
    time_end=time.time()
    process_time =np.round((time_end-time_start),2)
    print(process_time)
