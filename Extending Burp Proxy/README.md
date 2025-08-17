# Python & BurpSuite
To start importing custome Burp extensions, we will need to install <b>Jython</b>, a python2 implementation written in Java. There are many tutorials on how to install it 
and import it on your Burp instance. Next, to write an extension, we will have to take a look at Burp API documentation (Of course I did not read it all, just went over some 
Youtube videos and the BHP-2ED book). 

The first <b>1.Burp_Fuzzer.py</b> script in the directory demonstrates how to generate custom payloads for fuzzing when performing security testing. It works by testing 
SQLi, XSS, and inserting random chunks of the initial payload.

