# cut video into frames.
import os, sys, cv2, argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('viddir', help='video file path')
parser.add_argument('-to', help = 'output image format (.jpg or .bmp)', default = '.jpg')
parser.add_argument('-o' , help = 'output image directory + prefix', default = 'frame/img')

args = parser.parse_args()
vid = cv2.VideoCapture(args.viddir)

inpath = args.viddir.split('.')[0]
outpath = args.o.split('/')[0]

if not os.path.exists(inpath):
    os.mkdir(inpath)

os.system('rm -rf {}/{}'.format(inpath,outpath))
os.mkdir('{}/{}'.format(inpath,outpath))

cnt = 1

while(True):
    ret, img = vid.read()
    if ret:
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('{}{:03d}{}'.format(args.o,cnt,args.to), gray_frame)
        cnt += 1
    else:
        break

vid.release()