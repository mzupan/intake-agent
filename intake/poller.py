from tail import TailThread
from urllib import urlencode

import urllib
import urllib2
import threading
import time
import ConfigParser
import os
import sys

try:
    import json
except:
    import minijson as json


headers = {
    'User-Agent': 'InTake Agent v0.1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html, */*',
}


class Poller:
    def __init__(self, debug=False):
        self.config = {}
#        self.debug = debug

        #
        # load up the config
        #
        c = ConfigParser.ConfigParser()
    
        if os.path.exists("/etc/intake/config.conf"):
            c.read("/etc/intake/config.conf")
        else:
            print "Cannot find the config file at /etc/intake/config.conf"
            sys.exit()
    
        
        #
        # the only 3 configs that matter now
        #
        # api_url / api_user / api_key
        #
        self.config['api'] = {}
        self.config['api']['url'] = c.get('API', 'url')

        #
        # encoding serverid
        #
        self.config['id'] = c.get('API', 'uuid')
        if self.config['id'] == "":
            from socket import gethostname
            import uuid
    
            self.hostname = gethostname()
            self.id = uuid.uuid3(uuid.NAMESPACE_DNS, self.hostname)

            #
            # write it to the config now
            #
            c.set('API', 'uuid', self.id)
            self.config['id'] = str(self.id)
            
            with open('/etc/intake/config.conf', 'wb') as configfile:
                c.write(configfile)

        #
        # setting up the config dict
        #
        #
        self.config['logs'] = []

        #
        # thread container
        #
        self.threads = []
        
    def runChecks(self, s, firstRun=False):
        try:
            postData = urllib.urlencode({'server': self.id, 'host': self.hostname})
            request = urllib2.Request(self.config['api']['url'], postData, headers)
            response = urllib2.urlopen(request)

            j = json.loads(response.read())
        except Exception, err:
            print err
            #
            # temp till we get django up and running
            #
            j = []

        for log in j:
            if log not in self.config['logs']:
                self.config['logs'].append(log)
                
                #
                # launch off a new tail client
                #
                thread = TailThread(self.config, log)
                thread.start()
                self.threads.append(thread)
        
        #
        # clean up the threads if we no longer need to tail any logs
        #
        for thread in self.threads:
            if thread.log not in j:
                thread.done = True
                self.threads.remove(thread)
        
        s.enter(30, 1, self.runChecks, (s, False))

    def shutdown(self):
        for thread in self.threads:
            thread.done = True
