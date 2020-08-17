# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 13:50:24 2020

@author: 2007006
"""

import cv2
import numpy as np
import time
from numba import jit,njit

#相关操作
#由于使用的高斯函数圆对称，因此相关操作和卷积操作结果相同
class SSIM():
    def __init__(self):
        self.raw = np.fromfile('C:\\Users\\2007006\\Desktop\\Input\\HOS9B57684-05-VGH12-Vcom-6-VGL-2\\TemporalNoise_W3072H3072F30.raw', dtype='int16', sep="")
        self.img512 = np.fromfile('C:\\Users\\2007006\\Desktop\\circle-50\\afterOF512_30frame.raw', dtype='int16', sep="")
        self.img256 = np.fromfile('C:\\Users\\2007006\\Desktop\\M5_256_30frames.raw', dtype='int16', sep="")
        self.img32 = np.fromfile('C:\\Users\\2007006\\Desktop\\M5_32_30frames.raw', dtype='int16', sep="")                
        self.CY = np.fromfile('C:\\Users\\2007006\\Desktop\\Denoise_AUOPlatformForIntern_v2_2020_8_4_09_31_43_209\\HOS9B57684-05-VGH12-Vcom-6-VGL-2\\PlatformDenoise_TemporalNoise_W3072H3072F30.raw', dtype='int16', sep="")       
    
    def read_arr(self,array,numb):
        temp =array[0+numb*9437184:9437184+numb*9437184]
        arr = np.reshape(temp,(3072,3072))
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
    
M5_512=np.array([])
M5_256=np.array([])
M5_32=np.array([])
M5_CY= np.array([])    
M5_CY_LA= []
 
x = SSIM()

for i in range(30):
    time_start=time.time()
# get current numb i of array
    rawimg=x.read_arr(x.raw,i)
    img512=x.read_arr(x.img512,i)
    img256=x.read_arr(x.img256,i)
    img32=x.read_arr(x.img32,i)
    imgCY  =x.read_arr(x.CY,i)
# do ssim
    M512 = x.ssim(rawimg,img512)
    M256 = x.ssim(rawimg,img256)
    M32  = x.ssim(rawimg,img32)
    MCY = x.ssim(rawimg,imgCY)
    CYlarry = x.ssim(imgCY,img32)
# connect ssim output 
    M5_512=np.append(M5_512,M512)
    M5_256=np.append(M5_256,M256)
    M5_32=np.append(M5_32,M32)
    M5_CY= np.append(M5_CY,MCY)
    M5_CY_LA = np.append(M5_CY_LA,CYlarry)
    time_end=time.time()
    process_time =np.round((time_end-time_start),2)
    print(process_time)


del M512,M256,M32,MCY,rawimg,img512,img256,img32,imgCY
##==================save result to excell==================
#import pandas as pd
#df1 = pd.DataFrame([M5_512,M5_256,M5_32,M5_CY,M5_self],
#                   index=['method5_512', 'method5_256','method5_32','CY','rawbyraw'],
#                   columns=range(1,31))
#df1.to_excel("U:\\M5SSIM.xlsx")
#==========================================================