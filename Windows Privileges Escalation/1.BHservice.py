import os
import servicemanager
import shutil
import subprocess
import sys

import win32event
import win32service
import win32serviceutil

SRCDIR = 'C:\\Users\\kal\\work'
TGTDIR = 'C:\\Windows\\TEMP'

class BHServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "BHService"
    _svc_display_name_ = "Black Hat Service"
    _svc_description_ = ("Executes VBScripts at regular intervals." +
                        " What could possibly go wrong?")

    # Initialize the (win32serviceutil.ServiceFramework) framework and defines 3 methods:
    def __init__(self, args):
        # Define script location.
        self.vbs = os.path.join(TGTDIR, 'bhservice_task.vbs')
        # Set time out for 1 minute
        self.timeout = 1000 * 60

        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create Event Object.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    # Set the service and status and stop the service.
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    # Start the service and call the main method to run our task.
    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()

    #
    def main(self):
        # A loop that runs every minute (self.timeout).
        while True:
            ret_code = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Break if the service receives the stop signal.
            if ret_code == win32event.WAIT_OBJECT_0:
                servicemanager.LogInfoMsg("Service is stopping")
                break
            # While running:
            src = os.path.join(SRCDIR, 'bhservice_task.vbs')
            # Copy the file to target directory.
            shutil.copy(src, self.vbs)
            # Execute the script.
            subprocess.call("cscript.exe %s" % self.vbs, shell=False)
            # Remove the file.
            os.unlink(self.vbs)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(BHServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(BHServerSvc)
'''
    This is a skeleton script, you can modify it to a sneaky service further. It also requires the VBScript.
    To make it executable run the following:
    C:/Users/kal/work> pyinstaller -F --hiddenimport win32timezone BHservice.py
    
    Install the service and run it:
    C:/Users/kal/work> BHservice.exe install
    C:/Users/kal/work> BHservice.exe start
    
    To stop the service:
    C:/Users/kal/work> BHservice.exe stop
'''
