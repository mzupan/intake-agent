import time
import threading
import urllib
import urllib2

from os import stat
from os.path import abspath
from stat import ST_SIZE

try:
    import json
except:
    import minijson as json
    
headers = {
    'User-Agent': 'InTake Agent v0.1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html, */*',
}
 
class TailThread(threading.Thread):
    def __init__(self, config, log):
        threading.Thread.__init__(self)
        
        self.config = config
        self.log = abspath(log)
        self.done = False
        
        self.f = open(self.log, "r")
        file_len = stat(self.log)[ST_SIZE]
        self.f.seek(file_len)
        self.pos = self.f.tell()
        
        
    def _reset(self):
        self.f.close()
        self.f = open(self.log, "r")
        self.pos = self.f.tell()
    
    def run(self):
        while True:
            self.pos = self.f.tell()
            line = self.f.readlines()

            if not line:
                if stat(self.log)[ST_SIZE] < self.pos:
                    self._reset()
                else:
                    time.sleep(5)
                    self.f.seek(self.pos)
            else:
                j = json.dumps({
                                'log': self.log,
                                'line': line
                                })

                postData = urllib.urlencode({'action': 'add', 'server': self.config['id'], 'log': j})
                request = urllib2.Request(self.config['api']['url'], postData, headers)
                response = urllib2.urlopen(request)
        
            
            if self.done:
                break