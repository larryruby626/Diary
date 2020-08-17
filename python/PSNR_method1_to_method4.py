# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 13:29:44 2020

@author: 2007006
"""
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import math
import cv2
class PSNR():
    def __init__(self):
        self.A = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2_6processdata\\raw2.raw', dtype='int16', sep="")
        self.m1    = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\method1_30frame.raw', dtype='int16', sep="")
        self.m2_1  = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\method2_1time_30.raw', dtype='int16', sep="")
        self.m2_2  = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\method2_2time_30.raw', dtype='int16', sep="")
        self.m3    = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\method3_30frame.raw', dtype='int16', sep="")
        self.m4_32 = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\M4_32_30frame.raw', dtype='int16', sep="")
        self.m4_16 = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\M4_16_30frame.raw', dtype='int16', sep="")

    def read_arr(self,arr,numb):
        temp =arr[0+numb*1779456:1779456+numb*1779456]
#        arr = np.reshape(temp,(3072,3072))
        return temp
    
     
        
    def psnr(self,target, ref, scale):
        # target:目標影象  ref:參考影象  scale:尺寸大小
        # assume RGB image
        target_data = ref
        ref_data =  target    
        
        diff = ref_data - target_data
        rmse = math.sqrt( np.mean(diff ** 2) )
        
        return 10*math.log10(255**2/rmse)
    
    
    def saveto_raw(self,out_arr,filename): 
        out_arr = np.asarray(out_arr, dtype=np.int16)
        path = 'C:\\Users\\2007006\\Desktop\\'+ filename+'.raw'
        out_arr.astype('int16').tofile(path)
    def cumsum(self,a):
        a = iter(a)
        b = [next(a)]
        for i in a:
            b.append(b[-1] + i)
        return np.array(b)
    
    def get_histogram(self,image, bins):
        # array with size of bins, set to zeros
        histogram = np.zeros(bins)
        
        # loop through pixels and sum up counts of pixels
        for pixel in image:
            histogram[pixel] += 1
        
        # return our final result
        return histogram        
    def historgram(self,arr):
        flat = arr 
        # show the histogram
#        plt.hist(flat, bins=50)
        
        hist = self.get_histogram(flat, 65536)
        
        # execute the fn
        cs = self.cumsum(hist)
        # display the result
        
        nj = (cs - cs.min()) * 255
        N = cs.max() - cs.min()
        
        # re-normalize the cdf
        cs = nj / N
        cs = cs.astype('uint8')
        # get the value from cumulative sum for every index in flat, and set that as img_new
        img_new = cs[flat]
        # we see a much more evenly distributed histogram
#        img_new = np.reshape(img_new, (1324,1344))
        return img_new
        
    def plot(self,ori,arr):
        tori = np.reshape(ori,(1324,1344))
        tarr= np.reshape(arr,(1324,1344))
        fig = plt.figure()
        fig.set_figheight(15)
        fig.set_figwidth(15)        
        fig.add_subplot(1,2,1)
        plt.imshow(tori, cmap='gray')
        
        # display the new image
        fig.add_subplot(1,2,2)
        plt.imshow(tarr, cmap='gray')
        
        plt.show(block=True)
        
    def plotx(self,m1,m2,m21,m3,m432,m416):
        fig = plt.figure()
  
        fig.add_subplot(3,3,1)
        
        plt.plot(range(0,30),(m1[:]))        
        # display the new image
        
        fig.add_subplot(3,3,2)
        plt.plot(range(0,30),(m2[:]))        
    
        fig.add_subplot(3,3,3)
        plt.plot(range(0,30),(m21[:]))        
        
        fig.add_subplot(3,3,4)
        plt.plot(range(0,30),(m3[:]))        
        
        fig.add_subplot(3,3,5)
        plt.plot(range(0,30),(m432[:]))        
        
        fig.add_subplot(3,3,6)
        plt.plot(range(0,30),(m416[:]))        
        
        plt.show(block=True)
X = PSNR()
#cypsnr = np.array([])
#jzpsnr = np.array([])
method1=np.array([])
method2_1=np.array([])
method2_2=np.array([])
method3 = np.array([])
method4_32 = np.array([])
method4_16 = np.array([])

for i in range(30):
    origin = X.historgram(X.read_arr(X.A,i))
    
    target = X.historgram(X.read_arr(X.m1,i))
    outtmep= X.psnr(origin,target,3072)
    method1 = np.append(method1,outtmep)
    
    target = X.historgram(X.read_arr(X.m2_1,i))
    outtmep= X.psnr(origin,target,3072)
    method2_1 = np.append(method2_1,outtmep)    
    
    target = X.historgram(X.read_arr(X.m2_2,i))
    outtmep= X.psnr(origin,target,3072)
    method2_2 = np.append(method2_2,outtmep)    
    
    target = X.historgram(X.read_arr(X.m3,i))
    outtmep= X.psnr(origin,target,3072)
    method3 = np.append(method3,outtmep)    
     
    target = X.historgram(X.read_arr(X.m4_32,i) )
    outtmep= X.psnr(origin,target,3072)
    method4_32 = np.append(method4_32,outtmep)        
    
    target = X.historgram(X.read_arr(X.m4_16,i) )
    outtmep= X.psnr(origin,target,3072)
    method4_16 = np.append(method4_16,outtmep)      
#    noise = np.random.normal(0, 200, target.shape)
#    new_signal = target + noise
#    psnr_V,rmse= X.psnr(origin,new_signal,3072)
#    print("The CY "+str(i)+" psnr is :" + str(psnr_V))
#    cypsnr = np.append(cypsnr,psnr_V)
#    
#    target2 = X.read_arr3(i)
#    psnr_V2,diff= X.psnr(origin,target2,3072)
#    print("The JZ "+str(i)+" psnr is :" + str(psnr_V2))
#    jzpsnr = np.append(jzpsnr,psnr_V2)    

del target

# ---------------------------------put pixels in a 1D array by flattening out img array----------------------------------

xmin, xmax, num = 0,30,30# 設定繪圖範圍、取點數
x = np.linspace(xmin, xmax, num)                          # 產生x
plt.figure(figsize=(30,15))                 # 設定圖片尺寸
plt.xlabel('frame number of rawfile', fontsize = 16)                        
plt.ylabel('PSNR(dB)', fontsize = 16)                        # 設定坐標軸標籤
# 設定坐標軸標籤
plt.xticks(fontsize = 12)                                 # 設定坐標軸數字格式
plt.yticks(fontsize = 12)
plt.title("PSNR")
#plt.ylim(37,39)                                          # 設定y軸繪圖範圍
# 繪圖並設定線條顏色、寬度、圖例
line0, = plt.plot(method1[:], linewidth = 1, label = 'method1')
line1, = plt.plot(method2_1[:], linewidth = 1, label = 'method2_1')             
line2, = plt.plot(method2_2[:], linewidth = 1, label = 'method2_2')
line3, = plt.plot(method3[:], linewidth = 1, label = 'method3')
line4, = plt.plot(method4_32[:], linewidth = 1, label = 'method4_32')
line5, = plt.plot(method4_16[:], linewidth = 1, label = 'method4_16')

plt.legend(handles = [line0,line1, line2,line3,line4,line5], loc='upper right')

plt.show()    
#-------------------------------------------------------------------------------------------------------------------------          