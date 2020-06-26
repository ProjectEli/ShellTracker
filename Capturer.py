# ref[1]: https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
# ref[2]: http://pythonstudy.xyz/python/article/406-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%B2%98%EB%A6%AC-Pillow

# required modules
# pypiwin32 (구 win32api): pip install pypiwin32
# win32gui: 위 패키지 설치 후 Python\Python38-32\Scripts\pywin32_postinstall.py 실행 (필자는 관리자권한 powershell에서 cmd켜고 실행함)
# Image (구 PIL): pip install image


import win32gui, win32ui
from ctypes import windll
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

#result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
print(result)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)

if result == 1:
    im.show()
    # im.save('알리샤test.png')