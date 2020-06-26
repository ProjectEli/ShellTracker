# ref[1]: https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
# ref[2]: http://pythonstudy.xyz/python/article/406-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%B2%98%EB%A6%AC-Pillow
# ref[3]: https://pythonpath.wordpress.com/2012/09/17/pil-image-to-cv2-image/
# ref[4]: https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/

# required modules
# pypiwin32 (구 win32api): pip install pypiwin32
# win32gui: 위 패키지 설치 후 Python\Python38-32\Scripts\pywin32_postinstall.py 실행 (필자는 관리자권한 powershell에서 cmd켜고 실행함)
# Image (구 PIL): pip install image


import cv2, win32gui, win32ui
from ctypes import windll
import numpy as np
from PIL import Image

hwnd = win32gui.FindWindow(None,'BlueStacks')
# 전체화면 쓰고싶을경우는 아래처럼
# left, top, right, bot = win32gui.GetClientRect(hwnd)

left, top, right, bot = win32gui.GetWindowRect(hwnd)
w = right - left
h = bot - top

# device context 읽기 (픽셀인식 가능하게)
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdc
hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(saveBitMap)

arr = []

for k in range(200):
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    # print(result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    if result == 1:
        # im.show()
        # im.save('알리샤test.png')
        arr.append(im)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)

out = cv2.VideoWriter('aa.avi',cv2.VideoWriter_fourcc(*'DIVX'),30, (w,h))

for element in arr:
    element = cv2.cvtColor(np.asarray(element),cv2.COLOR_RGB2BGR)
    out.write(element)
out.release()