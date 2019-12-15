import numpy as np, random
import cv2, os, sys
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

symbol_num = 12
bit_num = 6 + 4*symbol_num + 2*symbol_num
frame_nums = [len(os.listdir('frames/800')), len(os.listdir('frames/1600')), len(os.listdir('frames/3200'))]

rand_3200_ratio = 0.5
rand_weights = [1-rand_3200_ratio, rand_3200_ratio]


experiment_times = 100
accs = np.zeros(experiment_times)
for exp_time in range(experiment_times):
    if exp_time % 10 == 9: print(exp_time)
    data = np.random.randint(2, size=symbol_num)*2 - 1
    
    bit_string = np.zeros(bit_num, dtype=np.int8)
    symbol_string = np.zeros(symbol_num, dtype=np.int8)
    
    #Preamble
    """
    for i in range(6):
        x = random.randint(0,frame_nums[1]-1)
        img = cv2.imread('frames/1600/{}.bmp'.format(x), cv2.IMREAD_GRAYSCALE)
        sig = extract1DSignal(naiiveCut(img))
        bit_string[i], _ = judgeBit(sig)
    """    
    #bit_string[:6] = random.choices([0,1], weights=rand_weights, k=6)
    
    #Data and SS
    for i in range(6, bit_num, 6):
        nums = np.zeros(3, np.int8)
        #Data
        for j in range(i, i+4):
            img = None
            if data[i//6-1] == -1:
                x = random.randint(0, frame_nums[0]-1)
                img = cv2.imread('frames/800/{}.bmp'.format(x), cv2.IMREAD_GRAYSCALE)
            else:
                x = random.randint(0, frame_nums[2]-1)
                img = cv2.imread('frames/3200/{}.bmp'.format(x), cv2.IMREAD_GRAYSCALE)
            
            sig = extract1DSignal(naiiveCut(img))
            bit_string[j], res = judgeBit(sig)
            nums[bit_string[j]+1] += 1
        
        if nums[0] > nums[2]: symbol_string[i//6-1] = -1
        elif nums[2] > nums[0]: symbol_string[i//6-1] = 1
        else: symbol_string[i//6-1] = random.choices([0,1], weights=rand_weights)[0]
        
        #SS
        """
        for j in range(i+4,i+6):
            x = random.randint(0, frame_nums[1]-1)
            img = cv2.imread('frames/1600/{}.bmp'.format(x), cv2.IMREAD_GRAYSCALE)
            sig = extract1DSignal(naiiveCut(img))
            bit_string[j], _ = judgeBit(sig)
        """
        #bit_string[i+4:i+6] = random.choices([0,1], weights=rand_weights, k=2)
    
    
    diff = np.dot(symbol_string, data)
    accs[exp_time] = len(diff[diff==1]) / symbol_num

print('mean accuracy {}%'.format(100*np.mean(accs)))