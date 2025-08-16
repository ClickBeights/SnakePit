# Hacking Web Applications

This section demonstrates how python scripts can be used for reconnaissance as well as unauthorized access on poorly implemented web applications. The first script in this 
section <b>1.Mapper.py</b> is a script that will crawl a local installation of WordPress to get some standard file and directories that could be interesting for Recon. This of course is based on filters we added in the script. The script will then make request to the targeted web application looking fot the files/directories we extracted from our local installation, if there is a match it gets printed on the screen.
<br>

## Brute-Forcing Directories and Files
The purpose of the second script <b>2.Bruter.py</b> in this folder is to enumerate folders and files on targeted a web application. This script will be used when we dp not have prior knowledge of the targeted web application, hence we cannot utilize the first one. The script accepts a wordlist and goes through the app making requests and only returning successful responses. The wordlist used in this script can be found at: [SVNDigger](https://cdn.invicti.com/app/uploads/2024/05/28102929/SVNDigger-1.zip?_gl=1*184utjo*_gcl_au*MTIzOTg3MTcyNi4xNzU0NDcwODAz*_ga*MTcyNDYxNjAwMi4xNzU0NDcwODA0*_ga_WWNQ4DL457*czE3NTQ0NzA4MDMkbzEkZzEkdDE3NTQ0NzA4NzQkajYwJGwwJGgw).
<br>
<br>

## Brute-Forcing HTML Form Authentication
The last script in the folder is desined specifically to asses password strength on a WordPress application. This script works against WordPress applications that use basic anti-brute-force techniques. The script is capable of holding the hidden token from the login form before submitting the password by leveraginthe LXML package. 
