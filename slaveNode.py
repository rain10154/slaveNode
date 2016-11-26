#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask

import os
import api
import task
import config
import netMonitor
import common

app = Flask(__name__)

userDict = {}

shell = {
    "start":"ssserver -c /etc/shadowsocks.json -d start",
    "stop":"ssserver -c /etc/shadowsocks.json -d stop",
    "restart":"ssserver -c /etc/shadowsocks.json -d restart"
}

ssConfig = {
    "server": "127.0.0.1",
    "local_port": 1081,
    "timeout": 300,
    "method": "aes-256-cfb"
}


def addUserTables():
    for k,v in userDict.items():
        netMonitor.add_iptables(k)


def writeDict2ss():
    ssConfig['port_password'] = userDict
    common.write_dict_to_file(config.get("ssFile"), ssConfig)


if __name__ == '__main__':
    api.postHostInfo()
    users = api.getAllUsers()

    if len(users) != 0:
        for k,v in users.items():
            port = int(str(k).split(":")[1])
            password = v['p']
            userDict[port] = password
        addUserTables()
        writeDict2ss()
        os.system(shell['start'])

    thread = task.myThread()
    thread.start()
    slave_port = int(config.get("slave_port"))

    app.run(port=slave_port,debug=False)



