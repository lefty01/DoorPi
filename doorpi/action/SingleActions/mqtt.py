# -*- coding: utf-8 -*-
# wal @ DoorPi forum

import logging
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

from doorpi.action.base import SingleAction
import doorpi
from time import sleep
import paho.mqtt.publish as publish

auth = {
  'username':'dein_user',
  'password':'dein_password'
}

def fire_command(hostname, port, mqtt, kind1, kind2):
        if kind2 == 'none':
                publish.single(mqtt, kind1, hostname = hostname, port = port, auth = auth)
        else:
                publish.single(mqtt, kind1, hostname = hostname, port = port, auth = auth)
                sleep(2)
                publish.single(mqtt, kind2, hostname = hostname, port = port, auth = auth)

def get(parameters):
        parameter_list = parameters.split(',')
        if len(parameter_list) is not 4 and not 5: return None
        hostname = parameter_list[0]
        port = parameter_list[1]
        mqtt = parameter_list[2]
        kind1 = parameter_list[3]

        if len(parameter_list) == 5:
                kind2 = parameter_list[4]
        else:
                kind2 = 'none'

        return MQTTAction(fire_command, hostname=hostname, port=port, mqtt=mqtt, kind1=kind1, kind2=kind2)

class MQTTAction(SingleAction):
        pass
