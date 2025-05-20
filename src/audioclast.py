#!/usr/bin/env python
import os
import time
import signal
import subprocess
from logger_setup import LoggerSetup
from pipewire_controller import PipeWireController
from vfs.fs import FS


class Audioclast:
    def __init__(self):
        self.log = LoggerSetup.get_logger(self.__class__.__name__)
        self.fs = FS()
        self.pid_file = self.fs.audioclast_pid_file
        self.log.info(f"PID file: {self.pid_file}")
        self.aplay_device = "hw:0,0"
        self.arecord_device = self.detect_mic()
        self.pipewire = PipeWireController()

    def detect_mic(self) -> str:
        try:
            with open("/proc/asound/cards", "r") as f:
                for line in f:
                    if "USB" in line or "Jieli" in line:
                        card_id = line.strip().split(" ")[0]
                        self.log.info(f"Detected USB mic on hw:{card_id},0")
                        return f"hw:{card_id},0"
        except Exception:
            self.log.exception("Could not detect USB mic")
        self.log.warning("Falling back to hw:2,0")
        return "hw:2,0"

    def is_running(self) -> bool:
        return self.pid_file.exists()

    def start(self):
        if self.is_running():
            self.log.warning("Audioclast already running.")
            return

        self.pipewire.stop()
        time.sleep(1)

        pipeline = (
            f"arecord -D {self.arecord_device} -r 48000 -f S16_LE -c 1 | "
            f"sox -t raw -r 48000 -e signed -b 16 -c 1 - -t wav -c 2 - remix - | "
            f"aplay -D {self.aplay_device}"
        )

        self.log.info("Starting audio monitoring loopback pipeline.")
        proc = subprocess.Popen(
            ["bash", "-c", pipeline],
            preexec_fn=os.setsid  # ključna linija: nova process grupa
        )

        with self.pid_file.open("w") as f:
            f.write(str(proc.pid))

    def stop(self):
        if not self.is_running():
            self.log.warning("Audioclast is not running.")
            return

        try:
            pid = int(self.pid_file.read_text().strip())
            self.log.info(f"Stopping Audioclast PID={pid} (killing process group)")
            os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            self.log.warning("Process group not found, maybe already dead.")
        except Exception as e:
            self.log.exception("Error while stopping audioclast")

        self.pid_file.unlink(missing_ok=True)
        self.pipewire.start()