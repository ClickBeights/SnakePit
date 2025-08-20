# GitHub as C2

This directory explores how GitHub can be used as a C2. This approach is known as a Out-Of-Band/Overt C2 as it uses already trusted and established platforms to achieve nefarious tasks. The way this will work is 
by writing a Trojan file, when executed on victim, it will visit the C2 repository and read the content of the config folder, it will then execute the modules (Payloads) based on the configuration read. Upon execution, 
the Trojan should write the results in the "data" folder in a file that has timestamp of execution as it's name. To do that, we will have to provide an Access Token to the Trojan.<br>
<br>
<b>Note:</b> Having Access Token available for the Trojan to use means most likely that anyone can use it the same way, make sure to limit the access as much as possible so that in case of leak, we already got what we 
want.
<br>
<br>

## The "config" Folder
This folder will contain configuration files in the form of JSON. each JSON file will declare modules (Payloads) that the Trojab will execute. The execution of course relies heavily on what JSON file was the 
Trojan instructde to read from as we may have many JSONs.
