import numpy as np
from random import randint
import cv2, os, sys

symbol_num = 12
bit_num = 6 + 4*symbol_num + 2*symbol_num

data, out_dir = np.random.randint(2, size=12), None
print('endcoded data:', end=' ')
print(data)

frame_nums = [len(os.listdir('frames/800')), len(os.listdir('frames/1600')), len(os.listdir('frames/3200'))]

try:
    out_dir = str(sys.argv[1])
except IndexError:
    print('Format: {} [output_dir]'.format(sys.argv[0]))
    sys.exit(1)

os.system('rm -fr {}'.format(out_dir))
os.mkdir(out_dir)

#Preamble
for i in range(6):
    x = randint(0,frame_nums[1]-1)
    out_path = os.path.join(out_dir, '{}.bmp'.format(i))
    os.system('cp frames/1600/{}.bmp {}'.format(x, out_path))

#Data and SS
for i in range(6, bit_num, 6):
    #Data
    for j in range(i, i+4):
        out_path = os.path.join(out_dir, '{}.bmp'.format(j))
        if data[i//6-1] == 0:
            x = randint(0, frame_nums[0]-1)
            os.system('cp frames/800/{}.bmp {}'.format(x, out_path))
        else:
            x = randint(0, frame_nums[2]-1)
            os.system('cp frames/3200/{}.bmp {}'.format(x, out_path))
    #SS
    for j in range(i+4,i+6):
        out_path = os.path.join(out_dir, '{}.bmp'.format(j))
        x = randint(0, frame_nums[1]-1)
        os.system('cp frames/1600/{}.bmp {}'.format(x, out_path))
