#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask,request

from common import logger
import os,jwt,json
import api
import task
import config
import netMonitor
import common
from os import path

app = Flask(__name__)

userDict = {}
secret =  config.get("secret")

shell = {
    "start":"ssserver -c /etc/shadowsocks.json -d start",
    "stop":"ssserver -c /etc/shadowsocks.json -d stop",
    "restart":"ssserver -c /etc/shadowsocks.json -d restart"
}

ssConfig = {
    "server": "0.0.0.0",
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


@app.route('/resetUser', methods=['GET'])
def addUser():
    users = api.getAllUsers()
    if len(users) != 0:
        logger.info("users:" + json.dumps(users))
        for k, v in users.items():
            port = int(str(k).split(":")[1])
            password = v['p']
            userDict[port] = password
        logger.info("start add user tables")
        addUserTables()
        logger.info("start write to ssfile")
        writeDict2ss()
        logger.info("start ss server, config is" + json.dumps(userDict))
        os.system(shell['restart'])
    return "ok"


@app.route('/addUser', methods=['POST'])
def addUser():
    data = jwt.decode(request.data, secret)
    userDict[int(data['port'])] = data['password']
    addUserTables()
    writeDict2ss()
    os.system(shell['restart'])
    return "ok"


@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    data = request.get_json()
    for x in data:
         del userDict[int(x)]
    writeDict2ss()
    os.system(shell['restart'])
    return "ok"

if __name__ == '__main__':
    res = json.loads(api.postHostInfo())
    if res.get('time') is not None:
        oldTime = int(res['time'])
        if oldTime != common.getOSTime() and path.isfile(config.get("flow_file")):
            os.remove(config.get("flow_file"))
    users = api.getAllUsers()

    if len(users) != 0:
        logger.info("users:" + json.dumps(users))
        for k,v in users.items():
            port = int(str(k).split(":")[1])
            password = v['p']
            userDict[port] = password
        logger.info("start add user tables")
        addUserTables()
        logger.info("start write to ssfile")
        writeDict2ss()
        logger.info("start ss server, config is" + json.dumps(userDict))
        os.system(shell['restart'])

    thread = task.myThread()
    thread.start()
    slave_port = int(config.get("slave_port"))

    app.run(host='0.0.0.0', port=slave_port,debug=False)



