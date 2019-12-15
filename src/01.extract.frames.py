import os, sys, cv2
import numpy as np

os.system('rm -fr frames')
os.mkdir('frames')

freqs = [800, 1600, 3200]
for freq in freqs:
    os.mkdir('frames/{}'.format(freq))
    cap = cv2.VideoCapture('original_vid/{}.MOV'.format(freq))
    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('frames/{}/{}.bmp'.format(freq, frame_num), gray_frame)
        frame_num += 1
            
    cap.release()