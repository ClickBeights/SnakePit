# Python & BurpSuite
To start importing custome Burp extensions, we will need to install <b>Jython</b>, a python2 implementation written in Java. There are many tutorials on how to install it 
and import it on your Burp instance. Next, to write an extension, we will have to take a look at Burp API documentation (Of course I did not read it all, just went over some 
Youtube videos and the BHP-2ED book). 

The first <b>1.Burp_Fuzzer.py</b> script in the directory demonstrates how to generate custom payloads for fuzzing when performing security testing. It works by testing 
SQLi, XSS, and inserting random chunks of the initial payload.
<br>
<br>

## Using Bing for Burp
MS Bing search engine has search capabilities that allow you to query Bing for all websites it finds on a single IP addres using the "IP" search modifier. Bing will also tell you all of the subdomains of a given domain if the "domain" seardch modifier was used. The second script in this directory demonstrates how to leerage bing for reconnaissance and gather as much information about subdomain as possoble effecively expanding our attack surface. As of today, bing has been updated to removi API key.
Refer: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
<br>
<br>

## Wordlist Generator
