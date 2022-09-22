from PIL import Image
import pytesseract
import sys
sys.path.append(r'C:\Users\sfb_s\src\genutils')
from get_windows import get_windows
from get_screenshot import get_screenshot
from post_image import post_image
import pytesseract
import base64

# return text using tesseract
# If you don't have tesseract executable in your PATH, include the
# following:
pytesseract.pytesseract.tesseract_cmd = \
        r'C:\Users\sfb_s\AppData\Local\Programs\Tesseract-OCR\tesseract'

def pull_window(name,crop=[]):
    
    # get window name
    framedata = get_windows(name)
    # scrape image frame
    frame = get_screenshot(framedata[0]['title'])
    
    if (len(frame)):
        # post image to webserver. add crop argument if necessary
        if crop:
            img = post_image(frame,'call_screenshot.png', \
            crop=crop)
        else:
            img = post_image(frame,'call_screenshot.png')

    topstring = pytesseract.image_to_string(img)
    str_array = topstring.split('\n')
    print(str_array)
    
    return str_array

if __name__ == "__main__":
    screenname = 'Watchlist'
    if len(sys.argv)>1:
        screenname = sys.argv[1]
    if len(sys.argv)>=5:
        crop = sys.argv[2:6]
        print(f"{screenname} crop: {crop}")
    pull_window(screenname,[int(n) for n in crop]) 
