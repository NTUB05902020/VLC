import cv2, os
import numpy as np
from util import naiiveCut


os.system('rm -fr cutt')
os.mkdir('cutt')


freqs = [800, 1600, 3200]
for freq in freqs:
    print(freq)
    os.mkdir('cutt/{}'.format(freq))
    frame_dir = 'frames/{}'.format(freq)
    
    center = [[], []]
    radius = []
    
    pics = os.listdir(frame_dir)
    for i in range(len(pics)):
        pic = '{}.bmp'.format(i)
        img = cv2.imread(os.path.join(frame_dir, pic), cv2.IMREAD_GRAYSCALE)
        print('    ', pic)
        cutimg = naiiveCut(img)
        cv2.imwrite('cutt/{}/{}.bmp'.format(freq, i), cutimg)
