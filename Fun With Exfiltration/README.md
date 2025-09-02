# Exfiltration
Extracting information is a crucial of a penetration testing as it serves as a proof of a successful exploitation. This directory demonstrates different ways to exfiltrate information we find useful. The first 
script in this directory is the <b>1.Crypter.py</b>. This script leverages a hybrid encryption process (Symmetric & Asymmetric). The script uses the <b>pycryptodomex</b> package for the encryption tasks.<br>
-We will be using the same script to encrypt data on victim (**Before Exfiltration**).
<br>
<br>

## Exfiltration Over Email
With the data encrypted using the previous script, it is now time to move it out. The second script in this directory carries 2 sending functions, the first function is a platform-independant one, sending data over regular SMPT. The second function works with Windows Specific technique using the **Win32Com** package to create an instance of outlook. Furthermore, the script deletes the email sent after submitting to clear tracks.<br>
-To view the content of the email after receiving them you must decrypt them using the same encryption script.
<br>
<br>

## Exfiltration Over File-Transfer
The third exfiltration script is <b>3.Transmit_Exfil.py</b>. In here, we use both **ftplib** for plaftform-independant exfiltration and **win32file** for windows functions. The plaftform-independant function facilitates FTP connection in a straigh forward function, the windows one however uses just connects to a port of a specified IP and then initiates the transfer.
<br>
<br>

## Exfiltration Over PastBin
The forth script on this directory demonstrates exfiltration over PastBin. This script will send the encrypted data by making a post on PastBin using the hard-coded credentials and API key. Since the data is encrypted, only we can view the original information. Now why PastBin ? Simply because it could bypass any blacklisting that a firewall or a proxy may have as PastBin is a well known site. The script creates an IE COM Object, for now the visibility of the execution is set to 1, for maximum stealth and background activity set the visibiity to 0.
<br>
<br>

## Putting it All Together
Finally, we tie all the exfiltration methods together with the **5.Exfil.py**. The script will exfiltrate data following the imports presented in the script. It is important to understand that all previous scripts must be in the same directory with the final script so that it can reach for them. 
