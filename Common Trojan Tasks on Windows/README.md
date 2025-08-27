# Post Exploitation Tasks
This directory demonstrates some of the most commmon tasks a trojan may run or be able to execute post initial exploitation. The scripts in this directory must be written and compiled on a winodws machine to better 
troubleshoot any errors. It is important to note that python scripts will not run on machines without a python installation. Therefore, it is important to compile these scripts into executables using the 
<b>PyInstaller</b> which will generate a 7+-MB executable.<br><br>
<b>Note!</b> These scripts are not meant to be used alone, they should be incorporated to the main trojan from the <b>GitHub Command and Control</b> directory.
<br>
<br>

## Key Logging
Logging key strokes is a staple when it comes to post exploitation tasks. The first script in this directory works by the 'keyboard' module to capure key presses. The script will keep logging for a set amount of time before printing all the information it gathered.
<br>
<br>

## Screenshots
The second script in this directory is <b>2.ScreenShotter.py</b> is yet another common post exploitation task, basically taking screenshots. The script leverages <b>PyWin32</b> package to make native Windows API calls. The grabber uses Windows Graphics Device Interface (GDI) to get the necessary variables for the screenshot.
<br>
<br>

## Python Shellcode
The third script in the directory is basically a python shellcode that is used in an exploit to execute raw shellcode without touching the filesystem. The execution steps are presented in form of comment in the script itself.
