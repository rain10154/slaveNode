import threading
import time
from common import logger
import json
import netMonitor
import api
import config

headers = {'content-type': 'application/json'}

fileName = "flows"

task_time = config.get("task_time")

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.policy = config.get("flow")

    def run(self):
        self.taskLoad()

    def taskLoad(self):
        self.timer_start()
        while True:
            time.sleep(1)

    def timer_start(self):
        t = threading.Timer(int(task_time), self.test_func)
        t.start()

    def test_func(self):
        logger.info("****** task begin!!!!")
        oldFlow = self.getOldFlow()
        logger.info("old flow:" + json.dumps(oldFlow))
        users = self.getUsers()
        logger.info("users:" + json.dumps(users))
        temp = netMonitor.get_original_flow()
        logger.info("new flow:" + json.dumps(temp))
        change = {}
        for k,v in users.items():
            nowFlow = self.countFlow(k, temp)
            logger.info('port:' + str(k) + ', now flow:' + str(nowFlow))
            if oldFlow.has_key(k):
                logger.info('old flow:' + str(oldFlow))
                if nowFlow != oldFlow[k]:
                    change[k] = nowFlow - oldFlow[k]
            else:
                change[k] = nowFlow
            oldFlow[k] = nowFlow
        logger.info("change flow:" + json.dumps(change))
        if change.__len__() != 0:
            api.postFlow(change)
            self.writeFlow2File(oldFlow)

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
        port = int(port)
        logger.info("count flow port:" + str(port) + ", flow:" + json.dumps(temp))
        flow_in = temp['flow_in'][port]
        flow_out = temp['flow_out'][port]
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



