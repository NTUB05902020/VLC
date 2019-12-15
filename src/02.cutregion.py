import cv2, os, glob, argparse
import numpy as np
from util import naiiveCut

parser = argparse.ArgumentParser()

parser.add_argument('imgdir',help='image file path')
parser.add_argument('-o' ,help = 'output image directory + name',default = 'cut/img')

args = parser.parse_args()
imgpath = args.imgdir

# File I/O:
images = glob.glob(imgpath+'*')
outpath = os.path.join(args.imgdir,'../',args.o.split('/')[0])

os.system('rm -rf {}'.format(outpath))
os.mkdir(outpath)

for fname in images:
    img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
    cutimg = naiiveCut(img)
    cv2.imwrite(os.path.join(outpath,fname.split('/')[-1]), cutimg)