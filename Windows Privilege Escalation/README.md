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
