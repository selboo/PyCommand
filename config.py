#!/usr/bin/env python
# encoding:utf-8
# AUTHOR written by Selboo 2015/03/12

from xml.dom.minidom import parse, parseString

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def readConfig():
    domfig    = parse('config.xml')
    config    = domfig.getElementsByTagName("config")[0]
    logfile   = config.getElementsByTagName("logfile")[0]
    munber    = config.getElementsByTagName("munber")[0]
    nsec      = config.getElementsByTagName("nsec")[0]
    db_ip     = config.getElementsByTagName("db_ip")[0]
    db_user   = config.getElementsByTagName("db_user")[0]
    db_pass   = config.getElementsByTagName("db_pass")[0]
    db_name   = config.getElementsByTagName("db_name")[0]
    db_tables = config.getElementsByTagName("db_tables")[0]
    return (getText(logfile.childNodes),
            getText(munber.childNodes),
            getText(nsec.childNodes),
            getText(db_ip.childNodes),
            getText(db_user.childNodes),
            getText(db_pass.childNodes),
            getText(db_name.childNodes),
            getText(db_tables.childNodes),
            )
