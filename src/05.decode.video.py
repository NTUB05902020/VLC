import cv2, os, sys, random
import numpy as np
import matplotlib.pyplot as plt
from util import cutRegion, extract1DSignal, judgeBit

def encodeHamming(num):
    errcorr, ret = 0, np.zeros(12, dtype=np.uint8)
    for ind in range(11, -1, -1):
        if ret[ind]==1 and ind!=0 and ind!=1 and ind!=3 and ind!=7:
            errcorr, ret[ind] = errcorr^(ind+1), 1
    
    if errcorr&8 > 0: ret[3] = 1
    if errcorr&4 > 0: ret[2] = 1
    if errcorr&2 > 0: ret[1] = 1
    if errcorr&1 > 0: ret[0] = 1
    return ret
    
def decodeHamming(bitstring):
    errcorr, num = 0, 0
    for i in range(12):
        if bitstring[i] == 1: errcorr = errcorr ^ (i+1)
        if i!=0 and i!=1 and i!=3 and i!=7:
            num = num*2+1 if bitstring[i]==1 else num*2
    
    if errcorr >= 12: return -2, num
    if errcorr > 0: num = num ^ (1<<(12-errcorr))
    bitstring2 = encodeHamming(num)
    for i in range(12):
        if bitstring[i] != bitstring2[i]: -2 if errcorr>0 else -1, num
    return 2 if errcorr>0 else 1, num

if __name__ == '__main__':
    try:
        frame_dir = str(sys.argv[1])
    except IndexError:
        print('Format: {} [frame_dir]'.format(sys.argv[0]))
        sys.exit(1)

    pics = sorted(os.listdir(frame_dir))
    
    atData, preamble_received = False, 0
    bitstring, decodeds, received = [], [], []
    
    for i,pic in enumerate(pics):
        if i % 2 == 0:
            gray_frame = cv2.imread(os.path.join(frame_dir,pic), cv2.IMREAD_GRAYSCALE)
            cutted = cutRegion(gray_frame)
            sig = extract1DSignal(cutted)
            
            bit, med_width = judgeBit(sig)
            received.append(bit)
            
            if bit == -1:
                bitstring, preamble_received = [], preamble_received+1
                if preamble_received > 2: atData = True
            elif atData == True:
                if len(bitstring) == 0: print('data start at {:>3d}'.format(i+1))
                bitstring, preamble_received = bitstring+[bit], 0
                if len(bitstring) == 12:
                    decodeds.append(bitstring)
                    bitstring, atData = [], False
                    print('data end at {:>3d}'.format(i+1))
    
    print('received')
    print(received)
    print('decodeds')
    for decoded in decodeds:
        print('    ', decoded, end='     ')
        ret, num = decodeHamming(decoded)
        if ret < 0:
            print('  Error! {:>2d}   {:>3d}'.format(ret, num))
        else:
            print('Correct! {:>2d}   {:>3d}'.format(ret, num))