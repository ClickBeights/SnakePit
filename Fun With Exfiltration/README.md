# Exfiltration

Extracting information is a crucial of a penetration testing as it serves as a proof of a successful exploitation. This directory demonstrates different ways to exfiltrate information we find useful. The first 
script in this directory is the <b>1.Crypter.py</b>. This script leverages a hybrid encryption process (Symmetric & Asymmetric). The script uses the <b>pycryptodomex</b> package for the encryption tasks.<br>
-We will be using the same script to encrypt data on victim (**Before Exfiltration**) and the decrypt the same data on our machine (**After Exfiltration**).
