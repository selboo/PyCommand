#!/usr/bin/env python
# encoding:utf-8
# AUTHOR written by Selboo 2015/03/12

import MySQLdb
import os
import sys
import time
import config

class PyLog:

    def __init__(self):
        logfile, munber, nsec, db_ip, db_user, db_pass, db_name, db_table = config.readConfig()
        self._nsec  = nsec
        self._ip    = db_ip
        self._user  = db_user
        self._pass  = db_pass
        self._name  = db_name
        self._teble = db_table

    def db_close(self):
        self.cursor.close()
        self.conn.close()

    def db_conn(self):
        try:
            self.conn = MySQLdb.connect(host=self._ip,user=self._user,passwd=self._pass,db=self._name,charset="utf8")
        except Exception, e:
            print e
            sys.exit();
        self.cursor = self.conn.cursor()

    def db_ping(self):
        while True:
            time.sleep(int(self._nsec))
            self.conn.ping()

    def db_insert(self, sqllist):
        globals().update(sqllist)
        sql = 'insert into %s.%s \
                    (id,HostName,RecordTime,CommandTime,LoginTime,LoginIP,LoginUser,LoginPid,CurrentUser,PathPWD,Command) \
                VALUES \
                    (NULL,"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                % \
                    (self._name, self._teble, HostName,RecordTime,CommandTime,LoginTime,LoginIP,LoginUser,LoginPid,CurrentUser,PathPWD,Command)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception,e:
            print e,sql
            return False
        
