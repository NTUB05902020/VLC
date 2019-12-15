import cv2, os, sys, random
import numpy as np
import matplotlib.pyplot as plt
from util import naiiveCut, extract1DSignal, judgeBit

symbol2str = lambda symbol: '1' if symbol==1 else ('0' if symbol==-1 else '?')


def printSymbols(symbol_string):
    for symbol in symbol_string: print(symbol2str(symbol), end=' ')
    print('')

def printSignal(symbol_string, bit_string):
    print('Preamble:', end='\n    ')
    for i in range(6): print(symbol2str(bit_string[i]), end=' ')
    print('\nSSs:')
    for i in range(10, len(bit_string), 6): print('    {} {}'.format(symbol2str(bit_string[i]), symbol2str(bit_string[i+1])))
    print('Data:')
    for i in range(6, len(bit_string), 6):
        print('    ', end='')
        for j in range(i,i+4): print(symbol2str(bit_string[j]), end=' ')
        print('  -->   {}'.format(symbol2str(symbol_string[i//6-1])))


try:
    video_dir = str(sys.argv[1])
except IndexError:
    print('Format: {} [video_dir]'.format(sys.argv[0]))
    sys.exit(1)

pics = sorted(os.listdir(video_dir)) # glob
total_bits = 12
total_frames = 6 + 4*total_bits + 2*total_bits
bit_string, symbol_string = [], []

rand_3200_ratio = 0.8
rand_weights = [1-rand_3200_ratio, rand_3200_ratio]


for i in range(total_frames):
    gray_frame = cv2.imread('{}/{}.bmp'.format(video_dir, i), cv2.IMREAD_GRAYSCALE)
    cutted = naiiveCut(gray_frame)
    sig = extract1DSignal(cutted)
    
    bit, res = judgeBit(sig)
    bit_string.append(bit)
    
    if i>=6 and (i-6)%6 == 4:
        nums = [0, 0, 0]  #[monenum, zeronum, onenum]
        for j in range(i-4, i): nums[bit_string[j]+1] += 1
        if nums[0] > nums[2]: symbol_string.append(-1)
        elif nums[0] < nums[2]: symbol_string.append(1)
        else: symbol_string.append(random.choices([-1,1], weights=rand_weights)[0])

printSignal(symbol_string, bit_string)