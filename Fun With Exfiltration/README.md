# Exfiltration

Extracting information is a crucial of a penetration testing as it serves as a proof of a successful exploitation. This directory demonstrates different ways to exfiltrate information we find useful. The first 
script in this directory is the <b>1.Crypter.py</b>. This script leverages a hybrid encryption process (Symmetric & Asymmetric). The script uses the <b>pycryptodomex</b> package for the encryption tasks.<br>
-We will be using the same script to encrypt data on victim (**Before Exfiltration**).
<br>
<br>

## Exfiltration Over Email

With the data encrypted using the previous script, it is now time to move it out. The second script in this directory carries 2 sending functions, the first function is a platform independant one, sending data over regular SMPT. The second function works with Windows Specific technique using the **Win32Com** package to create an instance of outlook. Furthermore, the script deletes the email sent after submitting to clear tracks.<br>
-To view the content of the email after receiving them you must decrypt them using the same encryption script.
