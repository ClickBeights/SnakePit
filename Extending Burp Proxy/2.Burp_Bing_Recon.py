from burp import IBurpExtender
from burp import IContextMenuFactory

from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem
from thread import start_new_thread

import json
import socket
import urllib

# Key can be obtained at: "https://www.microsoft.com/en-us/bing/apis/bing-web-search-api"
# Could have been retired around 11/08/2025, but check. It allows for 1000 'free' requests per month.
API_KEY = "<your api key>"
API_HOST = 'api.cognitive.microsoft.com'

# IContextMenuFactory allows for context menu when user clicks right click on the request.
# The menu should display "Send to Bing"
class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None

        # We set up our extension
        callbacks.setExtensionName("PYTHON2 Bing")
        # Register the menu handler.
        callbacks.registerContextMenuFactory(self)
        return

    # Receives 'IContextMenuInvocation' object and uses it to determine which HTTP request the user clicked.
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        # Render the menu item and handle the click event with big_menu method.
        menu_list.add(JMenuItem("Send to Bing", actionPerformed=self.bing_menu))
        return menu_list

    # This method is responsible for Bing query, output results, and add valid VHOSTS to scope.
    # It only triggers when the user clicks the context menu item we defined.
    def bing_menu(self, event):
        # Grab details of what the user clicked "Highlighted HTTP request".
        http_traffic = self.context.getSelectedMessages()
        print("%d requests highlighted" % len(http_traffic))
        # Retreive the host portion of each request and pass it to 'bing_search' method.
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()

            print("User selected host: %s" % host)
            self.bing_search(host)
        return

    # Determines if the host portion is an IP or a hostname.
    def bing_search(self, host):
        try:
            is_ip = bool(socket.inet_aton(host))
        except socket.error:
            is_ip = False

        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True
        # Qyery Bing for all VHOSTS that have the same IP address as the host.
        start_new_thread(self.bing_query, ('ip:%s' % ip_address,))
        # If ew received a domain, initiate a secondary search for subdomains.
        if domain:
            start_new_thread(self.bing_query, ('domain:%s' % host,))

    #
    def bing_query(self, bing_query_string):
        print('Performing Bing search: %s' % bing_query_string)
        # Burp HTTP API requires that we build the entire HTTP request as a string before sending it.
        http_request = 'GET https://%s/bing/v7.0/search?' % API_HOST
        # Encode our query:
        http_request += 'q=%s HTTP/1.1\r\n' % urllib.quote(bing_query_string)
        http_request += 'Host: %s' % API_HOST
        http_request += 'Connection:close\r\n'
        http_request += 'Ocp-Apim-Subscription-Key: %s\r\n' % API_KEY
        http_request += 'User-Agent: Mr. Sir\r\n\r\n'
        # Send the HTTP request to Microsoft servers.
        json_body = self._callbacks.makeHttpRequest(API_HOST, 443, True, http_request).tostring()
        # When the response returns, we split off the headers.
        json_body = json_body.split('\r\n\r\n', 1)[1]

        try:
            # Then pass them 'The headers' to JSON parser.
            response = json.loads(json_body)
        except (TypeError, ValueError) as err:
            print('No results from Bing: %s' % err)
        else:
            sites = list()
            if response.get('webPages'):
                sites = response['webPages']['value']
            if len(sites):
                # For each set of results, output some information abou the site.
                for site in sites:
                    print('*' * 100)
                    print('Name: %s       ' % site['name'])
                    print('URL: %s        ' % site['url'])
                    print('Description: %r' % site['snippet'])
                    print('*' * 100)

                    java_url = URL(site['url'])
                    # Add the site newely discovered automatically to scope if it wasn't there.
                    if not self._callbacks.isInScope(java_url):
                        print('Adding %s to Burp scope' % site['url'])
                        self._callbacks.includeInScope(java_url)
            else:
                print('Empty response from Bing.: %s' % bing_query_string)
        return
