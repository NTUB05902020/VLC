import sys, cv2, warnings
import numpy as np

gauss_size, gauss_sigma = 5, 10
gaussFilter = np.linspace(-gauss_size/2, gauss_size/2, num=5)
gaussFilter = np.exp(-np.square(gaussFilter) / (2*gauss_sigma**2))
gaussFilter = gaussFilter / np.sum(gaussFilter)

float2int = lambda val: int(round(val))

def naiiveCut(img):
    logged = np.log1p(img[:,540:640])
    m, M = np.min(logged), np.max(logged)
    out = (logged-m)*255/M
    out = out[out.shape[0]//4:out.shape[0]*3//4,:]
    return out.astype(np.uint8)

def cutRegion(img, ratiox=1.2, ratioy=1.2):
    gammaed = np.array(255*(img/255)**2, dtype='uint8')
    _, binarized = cv2.threshold(gammaed.astype(np.uint8), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    contours, _ = cv2.findContours(binarized, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    contours.sort(key=cv2.contourArea)
    
    (x,y), radius = cv2.minEnclosingCircle(contours[-1])
    reg_left, reg_right, dy = float2int(x - ratiox*radius), float2int(x + ratiox*radius), ratioy * radius
    reg_up, reg_down = float2int(y - dy), float2int(y + dy)
    
    clipped = binarized[reg_up:reg_down,reg_left:reg_right]
    return clipped
    #logged = np.log1p(clipped)
    #m, M = np.min(logged), np.max(logged)
    #out = (logged-m)*255/M
    #return out.astype(np.uint8), reg_left, reg_right, reg_up, reg_down, float2int(x), radius

def extract1DSignal(img):
    return np.convolve(img[:,img.shape[1]//2], gaussFilter, 'same')

def geoAltitude(signal, stride, slope):
    th, index_sta, siglen = stride*slope, 0, len(signal)
    for index_sta in range(0, siglen, stride):
        try:
            #print('{} - {}   {}'.format(signal[index_sta+stride], signal[index_sta], np.abs(signal[index_sta+stride]-signal[index_sta])))
            if np.abs(signal[index_sta+stride] - signal[index_sta]) > th: break
        except IndexError:
            print('Can\'t find first slope')
            sys.exit(1)
    
    plane_widths, isFlat = [], False
    for i in range(index_sta+stride, siglen, stride):
        try:
            if np.abs(signal[i+stride] - signal[i]) <= th:
                if not isFlat: isFlat, index_sta = True, i
            else:
                if isFlat:
                    isFlat, plane_widths = False, plane_widths+[i-index_sta];
                    #print('    {} {}'.format(index_sta, i))
        except IndexError:
            if len(plane_widths) > 0: return plane_widths
            print('No flats detected')
            sys.exit(1)

def getWidths(signal, stride, slope):
    wid1, wid2 = geoAltitude(signal[:220],1,1), geoAltitude(np.flip(signal[-220:]),1,1)
    return wid1 + wid2
    
def judgeBit(signal):
    widths = getWidths(signal,1,1)
    res, bit = [np.max(widths), np.median(widths)], 0
    if res[0]>47: bit = -1
    elif res[0]<=37 or res[1]>12: bit = 1
    return bit, res