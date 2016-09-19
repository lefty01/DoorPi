#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

import doorpi
import requests
import json
import base64
from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from requests.auth import HTTPBasicAuth
from doorpi.action.base import SingleAction

CONFIG = doorpi.DoorPi().config

def IPS(method, *parameters):
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

def IPS_MediaExists(key):
    response = IPS('IPS_MediaExists', key)
    return response.json()['result']

def IPS_GetMedia(key):
    response = IPS('IPS_GetMedia', key)
    return response.json()['result']['MediaType']

def IPS_SetMediaContent(key):
    try:
        if IPS_MediaExists(key) is not True: raise Exception("var %s doesn't exist", key)
        type = IPS_GetMedia(key)
        if type is None: raise Exception("type of var %s couldn't find", key)
        # http://www.ip-symcon.de/service/dokumentation/befehlsreferenz/variablenverwaltung/ips-getvariable/
        # Variablentyp (0: Boolean, 1: Integer, 2: Float, 3: String)
        elif type == 1:
            image = open('image.jpg', 'wb')
            camera = PiCamera()
            camera.start_preview()
            sleep(2)
            camera.capture(image)
            image.close()
            value = base64.b64encode(str(image))
            IPS('IPS_SetMediaContent', key, value)
            camera.close()
    except Exception as ex:
        logger.exception("couldn't send IpsRpc (%s)", ex)
        return False
    return True

def get(parameters):
    parameter_list = parameters.split(',')
    if len(parameter_list) is not 1: return None

    key = int(parameter_list[0])

    return IPS_SetMediaContentAction(IPS_SetMediaContent, key)

class IPS_SetMediaContentAction(SingleAction):
    pass
