# PyCommand 
Python Audit Recording system command 

## Create Tables

```
CREATE TABLE `command` ( 
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `HostName` varchar(50) NOT NULL, 
    `RecordTime` datetime NOT NULL, 
    `CommandTime` datetime NOT NULL, 
    `LoginTime` datetime NOT NULL, 
    `LoginIP` varchar(50) NOT NULL, 
    `LoginUser` varchar(20) NOT NULL, 
    `LoginPid` integer NOT NULL, 
    `CurrentUser` varchar(50) NOT NULL, 
    `PathPWD` varchar(50) NOT NULL, 
    `Command` longtext NOT NULL 
)
```

## Edit /etc/profile

```
[root@selboo ~]# cat /etc/profile | tail -n 20 
 
export HISTTIMEFORMAT="--- %F %T ---" 
export PROMPT_COMMAND=' 
{ 
        CommandTime=`history 1 | awk -F "---" "{print \\$2}" | sed -e "s/^ //;s/ $//g"` 
        Command=`history 1 | awk -F "---" "{print \\$3}" | base64` 
        CurrentUser=`id -un` 
        whoStr=(`who -u am i`) 
        LoginUser=${whoStr[0]} 
        LoginType=${whoStr[1]} 
        LoginYear=${whoStr[2]} 
        LoginMont=${whoStr[3]} 
        LoginPid=${whoStr[5]} 
        LoginIP=`echo ${whoStr[6]} | grep -oP "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"` 
        HostName=`hostname` 
        PathPWD=`pwd` 
        RecordTime=`date "+%Y-%m-%d %H:%M:%S"` 
        logger -p local6.notice -n 127.0.0.1 " {\"HostName\":\"$HostName\",\"RecordTime\":\"$RecordTime\",\"CommandTime\":\"$CommandTime\",\"LoginIP\":\"$LoginIP\",\"LoginUser\":\"$LoginUser\",\"LoginTime\":\"$LoginYear $LoginMont\",\"LoginPid\":\"$LoginPid\",\"CurrentUser\":\"$CurrentUser\",\"PathPWD\":\"$PathPWD\",\"Command\":\"$Command\" }" 
} 
'
[root@selboo ~]# 
```

## Edit /etc/rsyslog.conf

```
[root@selboo ~]# cat /etc/rsyslog.conf
# Provides UDP syslog reception
$ModLoad imudp
$UDPServerRun 514

# Provides TCP syslog reception
$ModLoad imtcp
$InputTCPServerRun 514
local6.* /var/log/command.log
[root@selboo ~]# 
```

## Start main.py

```
[root@selboo ~]# nohup python main.py &>/dev/null &
```