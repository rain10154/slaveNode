import requests,jwt,common,config,json
secret = str(config.get("secret"))
mainIp = str(config.get("main_ip"))
mainPort = str(config.get("main_port"))
slave_port = str(config.get("slave_port"))

headers = {'content-type': 'application/json'}

def getAllUsers():
    url = 'http://' + mainIp + ':' + mainPort + '/users'
    value = jwt.decode(requests.get(url=url, timeout=60).content, secret)
    if value is None or len(value) == 0:
        return {}
    else:
        res = {}
        for k,v in value.items:
            res[k] = json.loads(v)
        return res


def postHostInfo():
    url = 'http://' + mainIp + ':' + mainPort + '/host'
    data = {
        'mac':common.get_mac_address(),
        'time':common.getOSTime(),
        'port':slave_port
    }
    content =  requests.post(url=url, data=json.dumps(data), headers=headers, timeout=60)
    print 'post host info status :' + str(content.status_code) + ', response' + content.content


def postFlow(flows):
    url = 'http://' + mainIp + ':' + mainPort + '/flow'
    data = {
        'time':common.getOSTime(),
        'mac':common.get_mac_address(),
        'flow':flows
    }
    return requests.post(url=url, data=json.dumps(data), headers=headers, timeout=60)
