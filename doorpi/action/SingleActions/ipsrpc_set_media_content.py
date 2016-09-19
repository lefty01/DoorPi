#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

import doorpi
import requests
import json
from requests.auth import HTTPBasicAuth
from doorpi.action.base import SingleAction

CONFIG = doorpi.DoorPi().config

def ips_rpc_fire(method, *parameters):
    url = CONFIG.get('IP-Symcon', 'server')
    auth=HTTPBasicAuth(CONFIG.get('IP-Symcon', 'username'), CONFIG.get('IP-Symcon', 'password'))
    headers = {'content-type': 'application/json'}

    payload = {
        "method": method,
        "params": parameters,
        "jsonrpc": "2.0",
        "id": 0,
    }
    return requests.post(url, auth=auth, data=json.dumps(payload), headers=headers)

def ips_rpc_check_variable_exists(key):
    response = ips_rpc_fire('IPS_VariableExists', key)
    return response.json()['result']

def ips_rpc_get_variable_type(key):
    response = ips_rpc_fire('IPS_GetVariable', key)
    return response.json()['result']['VariableType']

def ips_rpc_get_variable_value(key):
    response = ips_rpc_fire('GetValue', key)
    return response.json()['result']

def ips_rpc_set_media_content(key, value):
    try:
        if ips_rpc_check_variable_exists(key) is not True: raise Exception("var %s doesn't exist", key)
        type = ips_rpc_get_variable_type(key)
        if type is None: raise Exception("type of var %s couldn't find", key)
        # http://www.ip-symcon.de/service/dokumentation/befehlsreferenz/variablenverwaltung/ips-getvariable/
        # Variablentyp (0: Boolean, 1: Integer, 2: Float, 3: String)
        elif type == 0:
            if value.lower() in ['true', 'yes', '1']: value = True
            else: value = False
        elif type == 1: value = int(value)
        elif type == 2: value = float(value)
        elif type == 3: value = str(value)
        else: value = str(
        ips_rpc_fire('IPS_SetMediaContent', key, value)
    except Exception as ex:
        logger.exception("couldn't send IpsRpc (%s)", ex)
        return False
    return True

def get(parameters):
    parameter_list = parameters.split(',')
    if len(parameter_list) is not 2: return None

    key = int(parameter_list[0])
    value = parameter_list[1]

    return IpsRpcSetMediaContentAction(ips_rpc_set_media_content, key, value)

class IpsRpcSetMediaContentAction(SingleAction):
    pass
