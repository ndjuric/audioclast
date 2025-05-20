#!/usr/bin/env python
import subprocess
from logger_setup import LoggerSetup


class PipeWireController:
    def __init__(self):
        self.log = LoggerSetup.get_logger(self.__class__.__name__)

    def stop(self):
        self.log.info("Stopping PipeWire services")
        subprocess.run(["systemctl", "--user", "stop", "pipewire.socket"])
        subprocess.run(["systemctl", "--user", "stop", "pipewire.service"])
        subprocess.run(["systemctl", "--user", "stop", "wireplumber.service"])

    def start(self):
        self.log.info("Starting PipeWire services")
        subprocess.run(["systemctl", "--user", "start", "pipewire.socket"])
        subprocess.run(["systemctl", "--user", "start", "pipewire.service"])
        subprocess.run(["systemctl", "--user", "start", "wireplumber.service"])
