import cv2, os
import numpy as np
from util import cutRegion
import matplotlib.pyplot as plt

freqs = [800, 1600, 3200]
for freq in freqs:
    #lefts, rights, ups, downs, xs, ys = [], [], [], [], [], []
    xs, ys, rs = [], [], []
    frame_dir = 'frames/{}'.format(freq)
    pics = os.listdir(frame_dir)
    for i in range(len(pics)):
        pic = '{}.jpg'.format(i)
        img = cv2.imread(os.path.join(frame_dir, pic), cv2.IMREAD_GRAYSCALE)
        print('    ', pic)
        cutimg, left, right, up, down, centerx, r = cutRegion(img)
        
        """
        lefts.append(left)
        rights.append(right)
        ups.append(up)
        downs.append(down)
        xs.append((left+right)/2)
        """
        xs.append(centerx)
        ys.append((up+down)/2)
        rs.append(r)
    """
    plt.clf()
    plt.plot(lefts, '.')
    plt.savefig('{:04d}_left.png'.format(freq))
    
    plt.clf()
    plt.plot(rights, '.')
    plt.savefig('{:04d}_right.png'.format(freq))
    
    plt.clf()
    plt.plot(ups, '.')
    plt.savefig('{:04d}_up.png'.format(freq))
    
    plt.clf()
    plt.plot(downs, '.')
    plt.savefig('{:04d}_down.png'.format(freq))
    """
    plt.clf()
    plt.plot(xs, '.')
    plt.savefig('{:04d}_x.png'.format(freq))
    
    plt.clf()
    plt.plot(ys, '.')
    plt.savefig('{:04d}_y.png'.format(freq))
    
    plt.clf()
    plt.plot(rs, '.')
    plt.savefig('{:04d}_r.png'.format(freq))