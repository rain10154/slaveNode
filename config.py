#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
filename = 'config'
fp = open(filename)
obj = json.load(fp)
fp.close()

def get(type):
    if obj.__contains__(type) is False:
        return None
    return obj[type]