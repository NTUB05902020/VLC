import cv2, os, glob, argparse
import numpy as np
from util import naiiveCut

parser = argparse.ArgumentParser()

parser.add_argument('imgdir',help='image file path')
parser.add_argument('-o' ,help = 'output image directory + name',default = 'cut/img')
parser.add_argument('-to', help = 'output image format (.jpg or .bmp)', default = '.jpg')

args = parser.parse_args()
imgpath = args.imgdir

# File I/O:
images = glob.glob(imgpath+'*')
outpath = args.o.split('/')[0]

if os.path.exists(outpath):
    os.system('rm -f {}/*'.format(outpath))
else:
    os.mkdir(outpath)


nof = len(images)

for fname in images:
    
    img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)

    cutimg = naiiveCut(img)

    cv2.imwrite('{}{:03d}{}'.format(args.o,cnt,args.to), cut_img)






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
