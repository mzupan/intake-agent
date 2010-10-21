#!/usr/bin/env python
 
import os
import sys
import time
import sched

#
# ignore warnings
#
import warnings
warnings.filterwarnings("ignore")

from daemon import Daemon
from poller import Poller

#
# config dictionary
#
config = {}

class MyDaemon(Daemon):     
    def run(self, debug=False):
        
        #
        # load up the poller
        #
        poller = Poller()
        
        
        #
        # using sched here since I think its thread safer then a lame while loop
        # with a sleep.
        #
        s = sched.scheduler(time.time, time.sleep)
        poller.runChecks(s, True)
        
        try:
            s.run()
        except (KeyboardInterrupt, SystemExit):
            poller.shutdown()


def main():
    daemon = MyDaemon('/var/run/intake.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'debug' == sys.argv[1]:
            daemon.run(debug = True)
        elif 'setup' == sys.argv[1]:
            setup()
        elif 'status' == sys.argv[1]:
            print
            print "need to do this"
            print
        else:
            print "Unknown command"
            sys.exit(2)
        
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|status|debug" % sys.argv[0]
        sys.exit(2)
        
#
# should never get called
#
if __name__ == "__main__":
    main()
