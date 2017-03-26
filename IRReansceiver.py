#!/usr/bin/python
import os

class IRReansceiver:
    def restartIRService(self):
        cmd = "sudo /etc/init.d/lirc restart"
        os.system(cmd)

    def sendIRCommand(self, device, cmd):
        cmd = "irsend SEND_ONCE {device} {cmd}".format(device = device, cmd = cmd)
        os.system(cmd)

