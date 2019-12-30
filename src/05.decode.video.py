import cv2, os, sys, random
import numpy as np
import matplotlib.pyplot as plt
from util import cutRegion, extract1DSignal, judgeBit

def encodeHamming(num):
    errcorr, ret = 0, np.zeros(12, dtype=np.uint8)
    for ind in range(11, -1, -1):
        if ind!=0 and ind!=1 and ind!=3 and ind!=7:
            if num & 1: errcorr, ret[ind] = errcorr^(ind+1), 1
            num = num >> 1
    
    if errcorr&8 > 0: ret[7] = 1
    if errcorr&4 > 0: ret[3] = 1
    if errcorr&2 > 0: ret[1] = 1
    if errcorr&1 > 0: ret[0] = 1
    return ret
    
def decodeHamming(bitstring):
    errcorr, num, inds = 0, 0, [2, 4, 5, 6, 8, 9, 10, 11]
    for ind in inds: num = num*2 + bitstring[ind]
    print('num = ', num)
    for i in range(12):
        #print((i+1)*bitstring[i], errcorr, end=' ')
        errcorr = errcorr ^ ((i+1)*bitstring[i])
        #print(errcorr)
    
    #print('     ', end='')
    #print(bitstring, end='    ')
    #print(num, errcorr, end='    ')
    #print('errcorr = {}'.format(errcorr))
    if errcorr > 12: return -1, bitstring, num
    if errcorr > 0:
        bitstring[errcorr-1] = 1 - bitstring[errcorr-1]
        for ind in inds: num = num*2 + bitstring[ind]
    
    bitstring2 = encodeHamming(num)
    #print(bitstring2)
    for i in range(12):
        #print(bitstring[i], bitstring2[i])
        if bitstring[i] != bitstring2[i]: return 0, bitstring2, num
    return 1, bitstring2, num

if __name__ == '__main__':
    try:
        frame_dir = str(sys.argv[1])
    except IndexError:
        print('Format: {} [frame_dir]'.format(sys.argv[0]))
        sys.exit(1)

    pics = sorted(os.listdir(frame_dir))
    
    preamble_received, startInd = 0, None
    bitstring, decodeds, received = [], [], []
    
    for i,pic in enumerate(pics):
        gray_frame = cv2.imread(os.path.join(frame_dir,pic), cv2.IMREAD_GRAYSCALE)
        cutted = cutRegion(gray_frame)
        sig = extract1DSignal(cutted)
        
        bit = judgeBit(sig)
        received.append(bit)
        
        if bit == -1:
            bitstring, preamble_received = [], preamble_received+1
            if preamble_received > 2: startInd = i+2
        else:
            if startInd != None:
                preamble_received = 0
                bitstring.append(bit)
                if len(bitstring) == 12:
                    decodeds.append([startInd, (i+1), bitstring.copy()])
                    bitstring, startInd = [], None
    
    print('received')
    print(received)
    print(received[65:])
    print('decodeds')
    for startInd, endInd, decoded in decodeds:
        print('\n\n                          ', np.array(decoded))
        ret, bitstring, num = decodeHamming(decoded)
        if ret <= 0:
            print('    {:>3d}  {:>3d}    Error! {:>2d}  {}  {:>3d}'.format(startInd, endInd, ret, bitstring, num))
        else:
            print('    {:>3d}  {:>3d}  Correct! {:>2d}  {}  {:>3d}'.format(startInd, endInd, ret, bitstring, num))
