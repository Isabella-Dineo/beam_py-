import numpy as np
import matplotlib.pyplot as plt 
import d2r
import patchwidth
import los
import patchcenter

def plotpatch(P, alpha, beta, hmin, hmax, npatch):
    """Function to plot the patches for a given height range. Using a 2d gaussian
    
       Args:
       -----
       P       : rotational period (seconds)
       alpha   : inclination angle (degrees)
       beta    : impact parameter (degrees)
       hmin    : minimum emission height (in km)
       hmax    : maximum emission height (in km)
       npatch  : number of emission patches
       
       Returns:
       --------
       A plot of the patches projected on to observational plane.
    
    """    
    
#   make a 2D array:
    x = np.linspace(-180, 180, num=500, endpoint=True)
    y = np.linspace(-180, 180, num=500, endpoint=True)
    X,Y = np.meshgrid(x,y)

#   patchcenter or mean of the plot from patch center:
    cx, cy = patchcenter.patch_center(P, hmin, hmax, npatch)

#   choose random patch widths (wp) depending on how patches specify:
    patchwidths = patchwidth.patch_width(P, hmin, hmax)
    #np.random.shuffle(patchwidths)
    if npatch > 1:
        np.random.shuffle(patchwidths)
        wp = patchwidths[0:npatch]

    if npatch == 1:
        wp = patchwidths 
    

#   wp == the spread (sigma)
#   project the sigmax and sigmay to the line of sight plane:
    xlos, ylos, thetalos = los.los(alpha, beta)
    sigmax = wp * d2r.sinD(thetalos)
    sigmay = wp * d2r.cosD(thetalos)
    
    
#   2D gaussian:
    peak = 5 # trial peak 
    a = ((d2r.cosD(thetalos) ** 2) / (2 * sigmax ** 2)) + ((d2r.sinD(thetalos) ** 2) / (2 * sigmay ** 2))
    b = (-(d2r.sinD(2 * thetalos)) / (4 * sigmax ** 2)) + ((d2r.sinD(2 * thetalos)) / (4 * sigmay ** 2))
    c = ((d2r.sinD(thetalos) ** 2) / (2 * sigmax ** 2)) + ((d2r.cosD(thetalos) ** 2) / (2 * sigmay ** 2))    

    if npatch > 1:
        for i in np.arange(len(cx)):
            Z = peak * np.exp(-(a[i] * (X - cx[i]) ** 2 - 2 * b[i] * (X - cx[i]) * (Y - cy[i]) + c[i] * (Y - cy[i]) ** 2))
            

    if npatch == 1:
        Z = peak * np.exp(-(a * (X - cx) ** 2 - 2 * b * (X - cx) * (Y - cy) + c * (Y - cy) ** 2)) 

#    if npatch == 0:
#        Z = peak * np.exp(-(a * (X - cx) ** 2 - 2 * b * (X - cx) * (Y - cy) + c * (Y - cy) ** 2)) 
        
    plt.figure()    
    plt.contour(X, Y, Z)
    plt.xlim(-90, 90)
    #plt.ylim(-50, 50)
    plt.grid()
    
    plt.figure()
    plt.grid()
    plt.imshow(Z)
    
    plt.show()    
 
  
    
    
############################ simple test ##########################
if __name__ == "__main__":
    P = 0.16
    alpha = 60
    beta = 0.5
    hmin = 50
    hmax = 950
    npatch = 3
    plotpatch(P, alpha, beta, hmin, hmax, npatch)
