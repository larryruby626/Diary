# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 08:07:18 2020

@author: 2007006
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 13:50:24 2020

@author: 2007006
"""

import cv2
import numpy as np
import time
from numba import jit,njit
import pandas as pd 


class SSIM():
    def __init__(self):
        #讀入檔案 請注意你檔案放置的位置請更改
        self.raw = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2.raw', dtype='int16', sep="")
        self.m1    = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\method1_30frame.raw', dtype='int16', sep="")
        self.m2_1  = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\method2_1time_30.raw', dtype='int16', sep="")
        self.m2_2  = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\method2_2time_30.raw', dtype='int16', sep="")
        self.m3    = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\method3_30frame.raw', dtype='int16', sep="")
        self.m4_32 = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\M4_32_30frame.raw', dtype='int16', sep="")
        self.m4_16 = np.fromfile('C:\\Users\\2007006\\Desktop\\raw2frame30\\M4_16_30frame.raw', dtype='int16', sep="")
        self.m5= np.fromfile('C://Users//2007006/Desktop//Method5_test_raw2.raw', dtype='int16', sep="")
    #
    def read_arr(self,arr,numb):
        temp =arr[0+numb*1779456:1779456+numb*1779456]
        arr = np.reshape(temp,(1324,1344))
        return arr
    
    def correlation(self,img,kernal):
        kernal_heigh = kernal.shape[0]
        kernal_width = kernal.shape[1]
        cor_heigh = img.shape[0] - kernal_heigh + 1
        cor_width = img.shape[1] - kernal_width + 1
        result = np.zeros((cor_heigh, cor_width), dtype=np.float64)
        for i in range(cor_heigh):
            for j in range(cor_width):
                result[i][j] = (img[i:i + kernal_heigh, j:j + kernal_width] * kernal).sum()
        return result
    
    #产生二维高斯核函数
    #这个函数参考自：https://blog.csdn.net/qq_16013649/article/details/78784791
    
    def gaussian_2d_kernel(self,kernel_size=11, sigma=1.5):
        kernel = np.zeros([kernel_size, kernel_size])
        center = kernel_size // 2
    
        if sigma == 0:
            sigma = ((kernel_size - 1) * 0.5 - 1) * 0.3 + 0.8
    
        s = 2 * (sigma ** 2)
        sum_val = 0
        for i in range(0, kernel_size):
            for j in range(0, kernel_size):
                x = i - center
                y = j - center
                kernel[i, j] = np.exp(-(x ** 2 + y ** 2) / s)
                sum_val += kernel[i, j]
        sum_val = 1 / sum_val
        return kernel * sum_val
    
    
    #ssim模型
    
    def ssim(self,distorted_image,original_image,window_size=11,gaussian_sigma=1.5,K1=0.01,K2=0.03,alfa=1,beta=1,gama=1):
        distorted_image=np.array(distorted_image,dtype=np.float64)
        original_image=np.array(original_image,dtype=np.float64)
        if not distorted_image.shape == original_image.shape:
            raise ValueError("Input Imagees must has the same size")
        if len(distorted_image.shape) > 2:
            raise ValueError("Please input the images with 1 channel")
        kernal=self.gaussian_2d_kernel(window_size,gaussian_sigma)
    
        #求ux uy ux*uy ux^2 uy^2 sigma_x^2 sigma_y^2 sigma_xy等中间变量
        ux=self.correlation(distorted_image,kernal)
        uy=self.correlation(original_image,kernal)
        distorted_image_sqr=distorted_image**2
        original_image_sqr=original_image**2
        dis_mult_ori=distorted_image*original_image
        uxx=self.correlation(distorted_image_sqr,kernal)
        uyy=self.correlation(original_image_sqr,kernal)
        uxy=self.correlation(dis_mult_ori,kernal)
        ux_sqr=ux**2
        uy_sqr=uy**2
        uxuy=ux*uy
        sx_sqr=uxx-ux_sqr
        sy_sqr=uyy-uy_sqr
        sxy=uxy-uxuy
        C1=(K1*255)**2
        C2=(K2*255)**2
        #常用情况的SSIM
        if(alfa==1 and beta==1 and gama==1):
            ssim=(2*uxuy+C1)*(2*sxy+C2)/(ux_sqr+uy_sqr+C1)/(sx_sqr+sy_sqr+C2)
            return np.mean(ssim)
        #计算亮度相似性
        l=(2*uxuy+C1)/(ux_sqr+uy_sqr+C1)
        l=l**alfa
        #计算对比度相似性
        sxsy=np.sqrt(sx_sqr)*np.sqrt(sy_sqr)
        c=(2*sxsy+C2)/(sx_sqr+sy_sqr+C2)
        c=c**beta
        #计算结构相似性
        C3=0.5*C2
        s=(sxy+C3)/(sxsy+C3)
        s=s**gama
        ssim=l*c*s
        return np.mean(ssim)
    
x = SSIM()
method1=np.array([])
method2_1=np.array([])
method2_2=np.array([])
method3 = np.array([])
method4_32 = np.array([])
method4_16 = np.array([])
method5 = np.array([])

for  i in range(30):
    rawimg=x.read_arr(x.raw,i)
    sm1= x.read_arr(x.m1,i)
    sm2_1 = x.read_arr(x.m2_1,i)
    sm2_2= x.read_arr(x.m2_2,i)
    sm3= x.read_arr(x.m3,i)
    sm4_16= x.read_arr(x.m4_16,i)
    sm4_32= x.read_arr(x.m4_32,i)
    
    rawsm1= x.ssim(rawimg,sm1)
    rawsm2_1= x.ssim(rawimg,sm2_1)
    rawsm2_2= x.ssim(rawimg,sm2_2)
    rawsm3= x.ssim(rawimg,sm3)
    rawsm4_16 = x.ssim (rawimg,sm4_16)
    rawsm4_32= x.ssim(rawimg,sm4_32)
    

    method1 = np.append(method1,rawsm1)
    method2_1 = np.append(method2_1,rawsm2_1)
    method2_2 = np.append(method2_2,rawsm2_2)
    method3 = np.append(method3,rawsm3)    
    method4_16 = np.append(method4_16,rawsm4_16)
    method4_32 = np.append(method4_32,rawsm4_32)
    
del rawimg,sm1,sm2_1,sm2_2,sm3,sm4_16,sm4_32

del rawsm1,rawsm2_1,rawsm2_2,rawsm3,rawsm4_16,rawsm4_32


df1 = pd.DataFrame([method1,method2_1,method2_2,method3,method4_16,method4_32],
                   index=['method1', 'method2_1','method2_2','method3','method4_16','method4_32'],
                   columns=range(1,31))
df1.to_excel("U:\\M1_4SSIM.xlsx")

del method1,method2_1,method2_2,method3,method4_16,method4_32



for  i in range(30):
    rawimg=x.read_arr(x.raw,i)
    m5 = x.read_arr(x.m5,i) 
    M5qq= x.ssim(rawimg,m5)
    method5 = np.append(method5,M5qq)










