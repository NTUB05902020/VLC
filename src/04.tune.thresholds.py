import cv2, os, sys
import numpy as np
import matplotlib.pyplot as plt
from util import naiiveCut, extract1DSignal, judgeBit


freqs, freq2right_bit = [800, 3200], {800: -1, 3200: 1}

for freq in freqs:
    print('freq = {}'.format(freq))
    right_bit, pics = freq2right_bit[freq], os.listdir('frames/{}'.format(freq))
    total_bits = len(pics)
    bits = np.zeros(total_bits, dtype=np.int8)
    for pic in pics:
        img = cv2.imread('frames/{}/{}'.format(freq, pic), cv2.IMREAD_GRAYSCALE)
        #print(pic)
        cutted = naiiveCut(img)
        sig = extract1DSignal(cutted)
        
        bit_index = int(pic.strip('.bmp'))
        bits[bit_index], _ = judgeBit(sig)


    for i in range(1,5):
        symbol_num = total_bits//i
        symbol_string = np.zeros(symbol_num, dtype=np.int8)
        for j in range(symbol_num):
            nums = np.zeros(3, dtype=np.int8)
            for k in range(i): nums[bits[j*i+k]+1] += 1
            if nums[0] > nums[2]: symbol_string[j] = -1
            elif nums[0] < nums[2]: symbol_string[j] = 1
        print('    i={}  cor: {:.2f}%'.format(i, 100*len(symbol_string[symbol_string==right_bit])/symbol_num), end='   ')
        print('err: {:.2f}%'.format(100*len(symbol_string[symbol_string==-right_bit])/symbol_num), end='   ')
        print('  ?: {:.2f}%'.format(100*len(symbol_string[symbol_string==0])/symbol_num))
        plt.clf()
        plt.plot(symbol_string, '.')
        plt.savefig('decoded_{}.png'.format(i))