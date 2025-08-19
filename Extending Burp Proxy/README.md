# Python & BurpSuite
To start importing custome Burp extensions, we will need to install <b>Jython</b>, a python2 implementation written in Java. There are many tutorials on how to install it 
and import it on your Burp instance. Next, to write an extension, we will have to take a look at Burp API documentation (Of course I did not read it all, just went over some 
Youtube videos and the BHP-2ED book). 

The first <b>1.Burp_Fuzzer.py</b> script in the directory demonstrates how to generate custom payloads for fuzzing when performing security testing. It works by testing 
SQLi, XSS, and inserting random chunks of the initial payload.
<br>
<br>

## Using Bing for Burp
MS Bing search engine has search capabilities that allow you to query Bing for all websites it finds on a single IP addres using the "IP" search modifier. Bing will also tell you all of the subdomains of a given domain if the "domain" seardch modifier was used. The second script in this directory demonstrates how to leerage bing for reconnaissance and gather as much information about subdomain as possoble effecively expanding our attack surface. As of today, bing has been updated to remove API key.
Refer: [Microsoft API retirement](https://learn.microsoft.com/en-us/previous-versions/bing/search-apis/bing-web-search/create-bing-search-service-resource)
<br>
<br>

## Wordlist Generator
The last script in this directory may as well be the most useful. <b>3.Burp_Wordlist_Generator.py</b> is a script that will crawl a website and generate a custom wordlist for for the site in question. The script reads the HTTP response of a responding host, strips HTML code, and uses regex expression to find all words starting with alphabetical character and 2 or more "word" characters specified by "<b>\w{2,}</b>" expression.<br>
-It also ensures no duplicate words exist in the wordlist by storing the wordlist list in a "set".
