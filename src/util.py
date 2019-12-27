import sys, cv2
import numpy as np

float2int = lambda val: int(round(val))


def cutRegion(img, ratiox=1, ratioy=1):
    img = img[100:-100,:]
    _, binarized = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    contours, _ = cv2.findContours(binarized, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    contours.sort(key=cv2.contourArea)
    
    (x,y), radius = cv2.minEnclosingCircle(contours[-1])
    reg_left, reg_right, dy = float2int(x - ratiox*radius), float2int(x + ratiox*radius), ratioy * radius
    reg_up, reg_down = float2int(y - dy), float2int(y + dy)
    
    clipped = binarized[reg_up:reg_down,reg_left:reg_right]
    return clipped

def extract1DSignal(img):
    return img[img.shape[0]//2,:]

def getWidths(signal):
    start = 0
    while True:
        if start == len(signal):
            print('Can\'t find first dark')
            sys.exit(1)
        elif signal[start] == 0: break
        else: start += 1
    
    widths = []
    for i in range(start+1, len(signal)):
        if signal[i] != signal[i-1]:
            if signal[i] == 255: widths.append(i-start+1)
            else: start = i
    
    if signal[-1] == 0: widths.append(len(signal)-start)
    return np.array(widths)

def judgeBit(signal):
    widths = getWidths(signal)
    res = np.median(widths)
    if res > 20: return 0, res
    elif res > 10: return -1, res
    else: return 1, res
    #elif res > 3.5: return 2, res
    #else: return 3, res