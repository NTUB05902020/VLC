import cv2, os, glob, argparse
import numpy as np
from util import cutRegion, extract1DSignal
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument('imgdir',help='image file path')
parser.add_argument('-o' ,help = 'output image directory + name',default = 'cut/')

args = parser.parse_args()
imgpath = args.imgdir

# File I/O:
images = glob.glob(imgpath+'*')
outpath = args.imgdir.strip('/').split('/')
outpath = os.path.join(*outpath[:-1], args.o)

os.system('rm -rf {}'.format(outpath))
os.mkdir(outpath)

for i,fname in enumerate(images):
    img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
    cutimg = cutRegion(img)
    cv2.imwrite(os.path.join(outpath,fname.split('/')[-1]), cutimg)
    if i == 0:
        sig = extract1DSignal(cutimg)
        plt.plot(sig, '.')
        plt.savefig('hello.png',)