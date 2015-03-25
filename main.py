#!/usr/bin/env python
# encoding:utf-8
# AUTHOR written by Selboo 2015/03/12

import db, config
import os, sys, re, threading
from pyinotify import WatchManager, Notifier, ProcessEvent
from pyinotify import IN_DELETE, IN_CREATE, IN_MODIFY
from re import compile, findall
from base64 import b64decode
    
class EventHandler(ProcessEvent):

    def process_IN_CREATE(self, event):
        #print "Create file: %s " % os.path.join(event.path,event.name)
        return 10

    def process_IN_DELETE(self, event):
        #print "Delete file: %s " % os.path.join(event.path,event.name)
        return 20

    def process_IN_MODIFY(self, event):
        #print "Modify file: %s " % os.path.join(event.path,event.name)
        return 30
        
class ReadLog:

    def __init__(self):
        logfile = config.readConfig()[0]
        self._logfile = logfile

    def log(self):
        f = self._logfile
        try:
            read_access_file = open(f, 'r')
            read_access_file.seek(2, os.SEEK_END)
            return read_access_file
        except IOError, e:
            print e
            sys.exit()

    def insert(self):
        logfile  = self.log()
        watch    = WatchManager()
        mask     = IN_DELETE | IN_CREATE | IN_MODIFY
        notifier = Notifier(watch, EventHandler())
        watch.add_watch(self._logfile, mask,rec=True)
        
        while True:
            try:
                notifier.process_events()
                for line in logfile.readlines():
                    try:
                        self.data.db_insert(self.redata(line))
                    except:
                        pass
                if notifier.check_events():
                    notifier.read_events()
            except KeyboardInterrupt:
                notifier.stop()
                break

    def redata(self, line):
        command_re  = compile( '(?={).*(?<=})' )
        return eval(findall( command_re, line )[0])

    def start(self):
        
        self.data = db.PyLog()
        self.data.db_conn()
        
        threadings = []

        threadings.append(threading.Thread(target=self.data.db_ping))
        threadings.append(threading.Thread(target=self.insert))

        for t in threadings:
            t.start()
            

if __name__ == '__main__':
    Commandlog = ReadLog()
    Commandlog.start()

