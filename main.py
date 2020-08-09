# 이미지/모듈 로드
import RPi.GPIO as GPIO
import cv2
import numpy as np
import os
from sklearn import linear_model
import time
from gtts import gTTS
from playsound import playsound
import os


def decode_braille_image(gray):
    debug_images = dict()
    expected_height = 150
    resize_rate = 150 / gray.shape[0]
    gray = cv2.resize(gray, (0, 0), fx=resize_rate, fy=resize_rate, interpolation=cv2.INTER_LINEAR)

    debug_images['resized'] = gray

    # 배경 이미지 도출
    #ax*x + b*x + c*y*y + d*y + e*x*y + f = v
    def func(k):
        y = k[0]
        x = k[1]
        return [x * x, y * y, x * y, x, y, 1]

    indices = np.indices(gray.shape).reshape([2, -1]).T
    src1 = np.apply_along_axis(func, 1, indices)
    src2 = gray.reshape(-1)

    ransac = linear_model.RANSACRegressor()
    ransac.fit(src1, src2)
    back = ransac.predict(src1).reshape(gray.shape)
    norm = cv2.convertScaleAbs((gray - back + 100))
    cv2.imshow('back', back.astype(np.uint8))
    cv2.imshow('norm', norm)

    # 이진화로 피쳐 추출
    thres = np.max(norm) * 0.2 + 100 * 0.8

    binary = cv2.threshold(norm, thres, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Binry", binary)
    debug_images['binary'] = binary

    #작은 특징이나 노이즈 제거
    binary = cv2.erode(binary, np.empty([0]), 3)
    binary = cv2.dilate(binary, np.empty([0]), 3)
    cv2.imshow('binary denoise', binary)

    #허프 라인으로 회전 보정

    img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    lines = cv2.HoughLines(binary, 1, np.pi / 360, 10, min_theta=np.pi*0.48, max_theta=np.pi*0.52)
    #lines = cv2.HoughLines(binary, 1, np.pi / 180, 30)
    if lines is not None:
        lines = lines.reshape([-1, 2])
        for line in lines[:10]:
            rho = line[0]
            theta = line[1]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)

        debug_images['hough'] = img

        theta_avr = np.average(lines[:10, 1])
        angle = (theta_avr - np.pi * 0.5) * 180 / np.pi
        rotmat = cv2.getRotationMatrix2D( (gray.shape[1] / 2, gray.shape[0] / 2), angle, 1)
        binary = cv2.warpAffine(binary,rotmat,(gray.shape[1],gray.shape[0]), flags=cv2.INTER_NEAREST)
        print('angle : ', angle)
        debug_images['rotated_binary'] = binary
    cv2.imshow("HOUGH", img)

    # 라벨을 추출하고 후보 센터점을 구함
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
    color = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(color, contours, -1, (0, 0, 255))
    cv2.imshow('contours', color)

    color = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    candis = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #크기가 작은 것 제외
        if area < 8:
            continue

        #모양이 너무 일그러진 것 제외
        ellipse = cv2.fitEllipse(cnt)
        s = min(ellipse[1])
        l = max(ellipse[1])
        if l / s > 3:
            continue

        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        candis.append((cx, cy))
        cv2.circle(color, (cx, cy), 3, (0, 0, 255), cv2.FILLED)

    candis = np.array(candis)

    debug_images['candidates'] = color
    cv2.imshow("center", color)
    # 가로 세로 그리드 파악
    color = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    def get_grid(ds):
        grid = []
        ds = np.sort(ds)
        for d in ds:
            #새로 추가
            if len(grid) == 0 or d - np.average(grid[-1]) > 3:
                grid.append([d])
            #기존 삽입
            else:
                grid[-1].append(d)
        grid = [int(np.average(i)) for i in grid]
        return grid

    grid_x = get_grid(candis[:, 0])
    grid_y = get_grid(candis[:, 1])


    def ransac_average(arr):
        avr = np.average(arr)
        while True:
            low = avr * 0.7
            high = avr * 1.3
            filtered = [i for i in arr if low < i < high]
            nu_avr = np.average(arr)
            if abs(nu_avr - avr) < 0.001:
                break
            avr = nu_avr
        return avr

    dists = [grid_x[i+1] - grid_x[i] for i in range(len(grid_x) - 1)]
    if len(dists) <= 2:
        norm_dist = min(dists)
    else:
        norm_dist = ransac_average(dists)

    del_grid_x = []
    for i in range(len(grid_x) - 1):
        dist = grid_x[i+1] - grid_x[i]
        if dist < norm_dist * 0.5:
            del_grid_x.append(grid_x[i])
    for d in del_grid_x:
        grid_x.remove(d)

    dists = [grid_x[i+1] - grid_x[i] for i in range(len(grid_x) - 1)]
    md = min(dists)


    while True:
        nu_grid_x = []
        for i in range(len(grid_x) - 1):
            dist = grid_x[i+1] - grid_x[i]
            if dist > norm_dist * 1.3:
                if i % 2 == 0:
                    nu_grid_x.append(int(grid_x[i] + md))
                else:
                    nu_grid_x.append(int(grid_x[i] + norm_dist))
                break
        grid_x += nu_grid_x
        grid_x.sort()

        if len(nu_grid_x) == 0:
            break
        


    for xs in grid_x:
        x = int(xs)
        cv2.line(color, (x, 0), (x, 10000), (0, 0, 255))
    for ys in grid_y:
        y = int(ys)
        cv2.line(color, (0, y), (10000, y), (0, 0, 255))
    debug_images['grid'] = color

    if len(grid_x) % 2 != 0:
        print('error of grid_x')
        return None, debug_images

    if len(grid_y) % 3 != 0:
        print('error of grid_y')
        return None, debug_images

    # 그리드 교차점을 중심으로 feature 파악
    w2 = int((grid_x[1] - grid_x[0]) * 0.4)
    grid = np.array(np.meshgrid(grid_x, grid_y)).reshape([2, -1])

    dots = np.zeros([len(grid_y), len(grid_x)], np.uint8)
    def count_area(g):
        gx = g[0]
        gy = g[1]
        count = np.count_nonzero(binary[gy-w2:gy+w2, gx-w2:gx+w2])
        print(gx, gy, count)
        return count > w2
            
    dots = np.apply_along_axis(count_area, 0, grid)

    color = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    for x, y, v in zip(grid[0], grid[1], dots):
        if v:
            cv2.circle(color, (x, y), 3, (0, 0, 255), cv2.FILLED)
    debug_images['final'] = color
    

    # 코드로 변환

    import korean_braille

    dots2d = dots.reshape([len(grid_y), -1]).astype(np.uint8)
    b_num = []
    print(dots2d)
    for y in range(0, len(grid_y), 3):
        row = []
        for x in range(0, len(grid_x), 2):
            d1 = dots2d[y, x] + dots2d[y+1, x] * 2 + dots2d[y+2, x] * 4
            d2 = dots2d[y, x+1] + dots2d[y+1, x+1] * 2 + dots2d[y+2, x+1] * 4
            d = d1 * 16 + d2
            row.append(d)

            if d in korean_braille.b1:
                print(hex(d), korean_braille.b1[d])
            elif d in korean_braille.b2:
                print(hex(d), korean_braille.b2[d])
            elif d in korean_braille.b3:
                print(hex(d), korean_braille.b3[d])
            else:
                print(hex(d), '??')

        b_num.append(row)

    final_korean = []
    for row in b_num:
        korean = korean_braille.encode(row)
        final_korean.append(korean)
        print(korean_braille.encode(row))

    ##################
    return final_korean, debug_images

def tts(text):

    tts = gTTS(text, lang='ko')

    tts.save('temp.mp3')
    playsound('temp.mp3')
    time.sleep(2)

    os.remove("temp.mp3")

if __name__ == '__main__':
    import time
    cap =cv2.VideoCapture(-1)
    
    if not cap.isOpened():
        print("카메라 감지 안됨. 종료")
        
    
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
           #  frame = cv2.flip(frame,1 )
            cv2.imshow("frame", frame)
            key = cv2.waitKey(1)
            
     #       if GPIO.input(18)==0:
            if key == ord("a"):
                start = time.time()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                korean, debug_images = decode_braille_image(gray)
                print(time.time()-start)
                if korean is not None:
                    for korean_ in korean:
                        print(korean_)
                        start = time.time()
                        tts(korean_)
                        print(time.time()-start)
           # first, last = os.path.splitext(filename)
           # grid_filename = 'dst/' + first + '_grid.jpg'
           # cv2.imwrite(grid_filename, debug_images['grid'])
           # cv2.waitKey(0)
            
            if key == 27:
                break
        else:
            print(ret)
    cap.release()



    for root, dirname, filenames in os.walk('test'):
        for filename in filenames:
            gray = cv2.imread(root + '/' + filename, cv2.IMREAD_GRAYSCALE)
            start = time.time()
            korean, debug_images = decode_braille_image(gray)
            print(time.time()-start)
            if korean is not None:
                print(korean)
                start = time.time()
                tts(korean[0])
                print(time.time()-start)
            first, last = os.path.splitext(filename)
            grid_filename = 'dst/' + first + '_grid.jpg'
            cv2.imwrite(grid_filename, debug_images['grid'])
            cv2.waitKey(0)
        
