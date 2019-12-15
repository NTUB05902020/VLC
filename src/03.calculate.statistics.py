import cv2, os, sys
import numpy as np
import pandas as pd

from util import extract1DSignal, getWidths

os.system('rm -fr statistics/time')
os.mkdir('statistics/time')
freqs = [800, 1600, 3200]
for freq in freqs:
    print(freq)
    pics = os.listdir('cutt/{}'.format(freq))
    pic_num = len(pics)
    stats = pd.DataFrame(index=[i for i in range(pic_num)], columns=['max','median','mean','len'])
    for pic in pics:
        print('    {}'.format(pic))
        img = cv2.imread('cutt/{}/{}'.format(freq, pic), cv2.IMREAD_GRAYSCALE)
        sig = extract1DSignal(img)
        widths = getWidths(sig, 1, 1)
        
        i = int(pic.strip('.jpg'))
        stats['max'][i] = np.max(widths)
        stats['median'][i] = np.median(widths)
        stats['mean'][i] = np.mean(widths)
        stats['len'][i] = len(widths)
    stats.to_csv('statistics/time/{}.csv'.format(freq))