from burp import IBurpExtender
from burp import IContextMenuFactory
from java.util import ArrayList
from javax.swing import JMenuItem
from datetime import datetime
from HTMLParser import HTMLParser

import re

# Helper class that allows us to strip the HTML tags from the HTTP response.
class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = list()

    # Stores the page text in a member variable.
    def handle_data(self, data):
        self.page_text.append(data)

    # This method adds the word stored in the 'Developer' comments to the password list.
    def handle_comment(self, data):
        # As we can see from the following line, 'handle_comment' calls for 'handle_data' under the cover.
        self.page_text.append(data)

    def strip(self, html):
        self.feed(html)
        # Does the stripping of page.
        return ' '.join(self.page_text)

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()
        # Starting eith a common password:
        self.wordlist = set(['password'])

        # Set up the extension.
        callbacks.setExtensionName("PYTHON2 Wordlist")
        callbacks.registerContextMenuFactory(self)
        return

    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem('Create Wordlist', actionPerformed=self.wordlist_menu))
        return menu_list

    # Takes selected HTTP and turn it into a base wordlist.
    def wordlist_menu(self, event):
        # Grabs the details of what the user clicked.
        http_traffic = self.context.getSelectedMessages()
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            # Saves the name of the responding host fot later.
            self.hosts.add(host)

            http_response = traffic.getResponse()
            if http_response:
                # Retrieve the HTTP response and feed it to the 'get_word' method.
                self.get_words(http_response)
        self.display_wordlist()
        return

    # Checks the response header for text based responses only.
    def get_words(self, http_response):
        headers, body = http_response.tostring().split('\r\n\r\n', 1)
        # Skip non-text responses.
        if headers.lower().find('content-type: text') == -1:
            return

        # Strips HTML code from the rest of the text.
        tag_stripper = TagStripper()
        page_text = tag_stripper.strip(body)

        # Use a regular expression to find words.
        words = re.findall(r'[a-zA-Z]\w{2,}', page_text)

        for word in words:
            # Filter out long words.
            if len(word) <= 12:
                # Save these words to the 'wordlist'.
                self.wordlist.add(word.lower())
        return

    # This method takes base word and turns it into a number of password guesses based on some common
    # password creation strategies. This example demonstrates creating a list of suffixes to add at the
    # end of the base word including current year.
    def mangle(self, word):
        year = datetime.now().year
        suffixes = ['', '1', '!', year]
        mangled = []

        # Go through each suffix and in capital letters for good measure.
        for password in (word, word.capitalize()):
            for suffix in suffixes:
                # And add it to the base word to create unique password attempts.
                mangled.append("%s%s" % (password, suffix))
        return mangled

    def display_wordlist(self):
        print("#!comment: PYTHON2 Wordlist for site(s) %s" % ", ".join(self.hosts))

        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)
        return
