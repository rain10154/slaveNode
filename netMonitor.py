#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import iptc
from common import logger
import json

def add_iptables(port):
    os.system("iptables -I INPUT  -p tcp --dport %s" %port)
    os.system("iptables -I OUTPUT -p tcp --sport %s" %port)


def get_original_flow():
    res={
            'flow_in':{},
            'flow_out':{},
            'status':'ok'
        }
    table = iptc.Table(iptc.Table.FILTER)

    chain_in = iptc.Chain(table, 'INPUT')
    chain_out = iptc.Chain(table, 'OUTPUT')

    table.refresh()

    for rule in chain_out.rules:
        try:
            if len(rule.matches)==1:
                sport = int(rule.matches[0].sport)
                res['flow_out'][sport] = rule.get_counters()[1]
        except Exception,inst:
            logger.info('[警告]未知的 iptables 规则，如果是其他软件添加的可以忽略。')
            logger.info(inst)
    for rule in chain_in.rules:
        try:
            if len(rule.matches)==1:
                dport = int(rule.matches[0].dport)
                res['flow_in'][dport] = rule.get_counters()[1]
        except Exception,inst:
            logger.info('[警告]未知的 iptables 规则，如果是其他软件添加的可以忽略。')
            logger.info(inst)
    logger.info("res:" + json.dumps(res))
    return res
