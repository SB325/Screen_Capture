import cv2 as cv  
import numpy as np  
import time  
import win32gui, win32ui, win32con  
from PIL import Image
import base64

def get_screenshot(win_name):

    hwnd = win32gui.FindWindow(None, win_name)
    if not hwnd:
        print('Capture: Window not found!')
        return []

    window_rect = win32gui.GetWindowRect(hwnd)
    print('window_rec',window_rect)
    w = window_rect[2] - window_rect[0]
    h = window_rect[3] - window_rect[1]

    wDC = win32gui.GetWindowDC(hwnd)
    print('wDC',wDC)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    print('dcObj',dcObj)
    cDC = dcObj.CreateCompatibleDC()
    print('cDC',cDC)
    dataBitMap = win32ui.CreateBitmap()
    print('dataBitMap',dataBitMap)
    dataBitMap.CreateCompatibleBitmap(dcObj,w, h)

    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w,h), \
        dcObj,(0,0),win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray,
            dtype='uint8')

    img.shape = (h,w,4)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd,wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = img[...,:3]

    return img

if __name__=="__main__":
    while(True):
        frame = get_screenshot('Live News Main@thinkorswim [build 1974]') 
        if (len(frame)):
            im = Image.fromarray(frame)
            im.save("C:\\apache-tomcat-8.5.75\webapps\ROOT\windowshot.png")
            data_uri = base64.b64encode(open('C:\\apache-tomcat-8.5.75\webapps\ROOT\windowshot.png', 'rb').read()).decode('utf-8')
            img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)

            text_file = open("C:\\apache-tomcat-8.5.75\webapps\ROOT\windowshot.html", "w")
            n = text_file.write(img_tag)
            text_file.close()

            print('screenshot saved!')
        time.sleep(5)    

