# Hacking Web Applications

This section demonstrates how python scripts can be used for reconnaissance as well as unauthorized access on poorly implemented web applications. The first script in this 
section <b>1.Mapper.py</b> is a script that will crawl a local installation of WordPress to get some standard file and directories that could be interesting for Recon. This 
of course is based on filters we added in the script. The script will then make request to the targeted web application looking fot the files/directories we extracted from 
our local installation, if there is a match it gets printed on the screen.
