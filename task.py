import threading
import time
from common import logger
import json
import netMonitor
import api
import config

headers = {'content-type': 'application/json'}

fileName = "flows"

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.policy = config.get("flow")

    def run(self):
        self.taskLoad()

    def taskLoad(self):
        self.timer_start()
        while True:
            time.sleep(2)

    def timer_start(self):
        t = threading.Timer(60*10, self.test_func)
        t.start()

    def test_func(self):
        oldFlow = self.getOldFlow()
        users = self.getUsers()
        temp = netMonitor.get_original_flow()
        change = {}
        for k,v in users:
            nowFlow = self.countFlow(k, temp)
            logger.debug('port:' + str(k) + ', now flow:' + str(nowFlow))
            if oldFlow.has_key(k):
                logger.debug('old flow:' + str(oldFlow))
                if nowFlow != oldFlow:
                    change[k] = nowFlow
            else:
                change[k] = nowFlow
            oldFlow[k] = nowFlow
        if change.__len__() != 0:
            api.postFlow(change)

    def getOldFlow(self):
        try:
            fp = open(fileName, 'r')
            flows = json.load(fp)
            fp.close()
            return flows
        except:
            return {}

    def writeFlow2File(self, flow):
        fp = open(fileName, 'w')
        json.dump(flow, fp)
        fp.close()

    def countFlow(self, port, temp):
        flow_in = temp['flow_in']
        flow_out = temp['flow_out']
        if self.policy == 0:
            return flow_in + flow_out
        elif self.policy == 1:
            return flow_in
        elif self.policy == 2:
            return flow_out

    def getUsers(self):
        fp = open(config.get("ssFile"), 'r')
        value = json.load(fp)
        fp.close()
        return value['port_password']



