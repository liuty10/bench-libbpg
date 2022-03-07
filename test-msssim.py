import sys
import cv2
import math
import numpy as np
from scipy import ndimage

# https://mubeta06.github.io/python/sp/_modules/sp/ssim.html
# https://cvnote.ddlee.cc/2019/09/12/psnr-ssim-python
# http://mubeta06.github.io/python/sp/ssim.html#example-usage
# https://stackoverflow.com/questions/32232269/how-exactly-scipy-ndimage-filters-convolve-works-for-3d-input

def psnr(img1, img2):
    # img1 and img2 have range [0, 255]
    mse = np.mean((img1 - img2)**2)
    if mse == 0:
        return float('inf')
    return 20 * math.log10(255.0 / math.sqrt(mse))

def ssim(img1, img2, cs_map=False):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2
    
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))

    if cs_map:
        return ssim_map.mean(), ((2.0*sigma12 + C2)/(sigma1_sq + sigma2_sq + C2)).mean()
    else:
        return ssim_map.mean()

def msssim(img1, img2):
    """This function implements Multi-Scale Structural Similarity (MSSSIM) Image 
    Quality Assessment according to Z. Wang's "Multi-scale structural similarity 
    for image quality assessment" Invited Paper, IEEE Asilomar Conference on 
    Signals, Systems and Computers, Nov. 2003 
    
    Author's MATLAB implementation:-
    http://www.cns.nyu.edu/~lcv/ssim/msssim.zip
    """
    level = 5
    weight = np.array([0.0448, 0.2856, 0.3001, 0.2363, 0.1333])
    downsample_filter = np.ones((2, 2, 2))/8.0
    mssim = np.array([])
    mcs = np.array([])
    im1 = img1
    im2 = img2
    print(im1.shape)
    for l in range(level):
        ssim_map, cs_map = ssim(im1, im2, cs_map=True)
        mssim = np.append(mssim, ssim_map)
        mcs = np.append(mcs, cs_map)
          
        filtered_im1 = ndimage.filters.convolve(im1, downsample_filter, mode='reflect')
        filtered_im2 = ndimage.filters.convolve(im2, downsample_filter, mode='reflect')
        im1 = filtered_im1[::2, ::2]
        im2 = filtered_im2[::2, ::2]
    return (np.prod(mcs[0:level-1]**weight[0:level-1])*(mssim[level-1]**weight[level-1]))

def main():
    img1 = np.asarray(cv2.imread(sys.argv[1]))
    img2 = np.asarray(cv2.imread(sys.argv[2]))
    print(img1.shape[0])
    print(img1.shape[1])
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    psnr_value 	  = psnr(img1, img2)
    ssim_value 	  = ssim(img1, img2)
    ms_ssim_value = msssim(img1, img2)
    print(f"PSNR:{psnr_value}. SSIM: {ssim_value}. MS-SSIM: {ms_ssim_value}.")

if __name__ == '__main__':
    sys.exit(main())
