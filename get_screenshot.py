import cv2 as cv  
import numpy as np  
import time  
import win32gui, win32ui, win32con  
from PIL import Image
import sys
sys.path.append(r'C:\Users\sfb_s\src\genutils')
import base64
from post_image import post_image
from sms import sms
from delay_hour import delay_hour

def get_screenshot(win_name, verbose=False):

    hwnd = win32gui.FindWindow(None, win_name)
    if not hwnd:
        print('Capture: Window not found!')
        return []

    window_rect = win32gui.GetWindowRect(hwnd)
    if verbose: print('window_rec',window_rect)
    w = window_rect[2] - window_rect[0]
    h = window_rect[3] - window_rect[1]

    wDC = win32gui.GetWindowDC(hwnd)
    if verbose: print('wDC',wDC)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    if verbose: print('dcObj',dcObj)
    cDC = dcObj.CreateCompatibleDC()
    if verbose: print('cDC',cDC)
    dataBitMap = win32ui.CreateBitmap()
    if verbose: print('dataBitMap',dataBitMap)
    dataBitMap.CreateCompatibleBitmap(dcObj,w, h)

    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w,h), \
        dcObj,(0,0),win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray,
            dtype='uint8')
    #img = np.fromstring(signedIntsArray,
    #        dtype='uint8')

    img.shape = (h,w,4)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd,wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = img[...,:3]

    return img

if __name__=="__main__":
    messager = sms()
    delay = delay_hour()

    while True:
        #delay.wait_between(3,19)
        frame = get_screenshot('Live News Main@thinkorswim [build 1976]') 
        if (len(frame)):
            img = post_image(frame,'call_screenshot.png',(),True)
        else:
            messager.send_sms('The TDA Live News screen NOT FOUND!')   
        time.sleep(10)
