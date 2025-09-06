# Windows Privilege Escalation

In this section, we will be domnstrating some privilege escalation techniques on Windows OS that can be abused using python scripts. Elevating privileges post exploitation is a no brainer during a penetration testing 
engagement.
<br>
<br>

## The Vulnerable Service
The first script in this directory **1.BHservice.py** is a vulnerable executable (Use PyInstaller) that will emulate common vulnerabilities found in large enterprise networks. The purpose of this script is to
periodicaly copy a script to a temporary directory and execute it from that directory. You can find more details regarding compiling and executing inside the script.
<br>
<br>

## Monitoring Processes
The monitoring script (**2.Process_Monitor.py**) leverageg WMI API to recieve callbacks when events occur. This way, we can monitor process creation, process owner, parent, process, ID, and much more. Most importantly however, we want to keep an eye out for privileged processes that call external files (VBScripts or Batch).
<br>
<br>

## Extended Monitoring
In this version of the monitoring script we added a function that will monitor for the privileges in the processes we monior. We can print out security token per process by using the following modules (**Win32security**, **Win32api**, **Win32con**) as demonstrated in the first function from the script.
<br>
<br>
