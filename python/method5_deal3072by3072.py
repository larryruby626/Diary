
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 08:00:21 2020

@author: 2007006
"""
import numpy as np
import copy
import time

class xray():
    
    def __init__(self):
#        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\HS_TemporalNoise.raw', dtype='int16', sep="")
#        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\N8reverse_30frame.raw', dtype='int16', sep="")
        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\Input\\HOS9B57684-05-VGH12-Vcom-6-VGL-2\\TemporalNoise_W3072H3072F30.raw', dtype='int16', sep="")
#        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\Input\\HOS9257676-17-VGH12-Vcom-6-VGL-2\\TemporalNoise_W3072H3072F30.raw', dtype='int16', sep="")
        self.ALL_median = np.median(self.A)
        self.std = np.std(self.A)
#========= get the pic_length of pic ==============
        self.raw_length = int((np.size(self.A))/9437184)
        
#========= read the current numb of picture (avoid to use too many memory)==============      
    def read_arr(self,numb):
        arr =np.zeros((3072,3072))
        temp =self.A[0+numb*9437184:9437184+numb*9437184]
        arr = np.reshape(temp,(3072,3072))
        return arr
#=========  1280*1280 translate to one line ==============
    def arr_to_row(self,arr): 
        out_arr =[]        
        for i in range(3072):
            for j in range(3072):
                out_arr.append((arr[i,j]))   
        return out_arr  
        
#========= save the one line data to file==============

    def saveto_raw(self,out_arr,filename): 
        out_arr = np.asarray(out_arr, dtype=np.int16)
        path = 'C:\\Users\\2007006\\Desktop\\'+ filename+'.raw'
        out_arr.astype('int16').tofile(path)
        
  
    def oneframe3072(self,arr):
        pic1=arr
# =====================減去中位數並且mark defect===============
        pic2 = copy.deepcopy(pic1) 
        pic3 = copy.deepcopy(pic1)
        pic3 = pic3 -self.ALL_median
        pic3=np.where(pic3>(3*self.std),666,pic3)
        pic3=np.where(pic3<(-3*self.std),666,pic3)
# =====================處理data line noise==================
        aa=np.zeros((3072,3072))
        for j in range(384):
            y1=0+8*j
            y2=8+8*j
            tt =pic3[:,y1:y2]
            aa[:,y1:y2] = np.mean(tt[np.where(tt != 666)])
            print((np.mean(tt[np.where(tt != 666)])))
        pic2[np.where(pic3 != 666)] -= aa[np.where(pic3 != 666)]
        
# ==========================================================
        pic2[np.where(pic3 != 666)] -=self.ALL_median
        N = 256 
        devide = int(3072/N)
# ==========================================================
        for i in range (3072):
            for j in range(devide):    
                ind = 0+j*N
                ind1 = N+j*N
#                x = np.where((pic2[i,ind:ind1]<3*std))
#                x = np.where((pic2[i,ind:ind1]>-3*std))
                temp_pic2 =pic2[i,ind:ind1]
                temp = np.median(temp_pic2[:])
                temp_pic2[np.where(temp_pic2 != 666)]  -= temp
#                pic2[i,ind:ind1] -= temp 
                pic2[i,ind:ind1] =temp_pic2
        pic2[np.where(pic3 != 666)] += self.ALL_median
        pic2 = np.where(pic2<0,0,pic2)    
        return pic2

    def reverse_oneframe3072(self,arr): #反轉處理先後順序(肇驛建議)
        pic1=arr
# =====================減去中位數並且mark defect===============
        pic2 = copy.deepcopy(pic1) 
        pic3 = copy.deepcopy(pic1)
        pic3 = pic3 -self.ALL_median
        pic3=np.where(pic3>(3*self.std),666,pic3)
        pic3=np.where(pic3<(-3*self.std),666,pic3)        
## ==========================================================
        pic2[np.where(pic3 != 666)] -=self.ALL_median
        N = 256 
        devide = int(3072/N)
## ==========================================================
        for i in range (3072):
            for j in range(devide):    
                ind = 0+j*N
                ind1 = N+j*N
#                x = np.where((pic2[i,ind:ind1]<3*std))
#                x = np.where((pic2[i,ind:ind1]>-3*std))
                temp_pic2 =pic2[i,ind:ind1]
                temp = np.median(temp_pic2[:])
                temp_pic2[np.where(temp_pic2 != 666)]  -= temp
#                pic2[i,ind:ind1] -= temp 
                pic2[i,ind:ind1] =temp_pic2
                
# =====================處理data line noise==================
        aa=np.zeros((3072,3072))
        for j in range(384):
            y1=0+8*j
            y2=8+8*j
            tt =pic3[:,y1:y2]
            aa[:,y1:y2] = np.mean(tt[np.where(tt != 666)])
    #        print((np.mean(tt[np.where(tt != 666)])))
        pic2[np.where(pic3 != 666)] -= aa[np.where(pic3 != 666)]         
        pic2[np.where(pic3 != 666)] += self.ALL_median
        pic2 = np.where(pic2<0,0,pic2)    
        return pic2        
        
if __name__ == '__main__':
   
    time_start=time.time()
    A = xray()
    narry = np.array([])

    for i in range(A.raw_length):
#    for i in range(1):

#        pic2 = A.oneframe3072(A.arr[i])
        pic = A.read_arr(i)
        pic=pic.astype(float)
        pic2 = A.oneframe3072(pic)
        
        onelinearr = A.arr_to_row(pic2)
        
        narry =np.append(narry,onelinearr)
        
    A.saveto_raw(narry,'outfilename')
    
    del onelinearr,narry
    
    time_end=time.time()
    process_time =np.round((time_end-time_start),2)
    print(process_time)

