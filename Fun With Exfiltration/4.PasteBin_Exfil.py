from win32com import client

import os
import random
import requests
import time

username = 'kali'
password = 'kaliWTF'
api_dev_key = 'cd3xxx001xxxx02'

def plain_paste(title, contents):
    login_url = 'https://pastebin.com/api/api_login.php'
    login_data = {
        'api_dev_key': api_dev_key,
        'api_user_name': username,
        'api_user_password': password,
    }

    # The response of the previous request contains the 'apu_user_key' required for making a paste.
    r = requests.post(login_url, data=login_data)
    api_user_key = r.text

    paste_url = 'https://pastebin.com/api/api_post.php'
    paste_data = {
        'api_paste_name': title,
        'api_paste_code': contents.decode(),
        'api_dev_key': api_dev_key,
        'api_user_key': api_user_key,
        'api_option': 'paste',
        'api_paste_private': 0,
    }
    r = requests.post(paste_url, data=paste_data)
    print(r.status_code)
    print(r.text)

# A helper function that ensures the browser finished its events
def wait_for_browser(browser):
    while browser.ReadyState != 4 and browser.ReadyState != 'complete':
        time.sleep(0.1)

# A helper function that makes the browser act in a somewhat random manner so it doesn't look programmed.
def random_sleep():
    time.sleep(random.randint(5, 10))

# Retrieves important information for authentication.
def login(ie):
    # Retrieves all elements in DOM.
    full_doc = ie.Document.all
    for elem in full_doc:
        # Looks for Username and Password fields.
        if elem.id == 'loginform-username':
            elem.setAttribute('value', username)
        elif elem.id == 'loginform-password':
            elem.setAttribute('value', password)

    random_sleep()
    if ie.Document.forms[0].id == 'w0':
        ie.document.forms[0].submit()
    wait_for_browser(ie)

# This function initiates the authentication to the platform.
def submit(ie, title, contents):
    # All the following content is to submit the post request.
    full_doc = ie.Document.all
    for elem in full_doc:
        if elem.id == 'postform-name':
            elem.setAttribute('value', title)

        elif elem.id == 'postform-text':
            elem.setAttribute('value', contents)

    if ie.Document.forms[0].id == 'w0':
        ie.document.forms[0].submit()
    random_sleep()
    wait_for_browser(ie)

# IE because it is installed by default on all Winodows machines.
def ie_paste(title, contents):
    # Create new instance of IE COM object.
    ie = client.Dispatch('InternetExplorer.Application')
    # 1 = Debugging and visible, 0 = Stealth process not visible.
    ie.Visible = 1

    ie.Navigate('https://pastebin.com/login')
    wait_for_browser(ie)
    login(ie)

    ie.Navigate('https://pastebin.com/')
    wait_for_browser(ie)
    submit(ie, title, contents.decode())

    # Kill IE process when done.
    ie.Quit()

if __name__ == '__main__':
    ie_paste('title', 'contents')
