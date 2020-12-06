#!/usr/bin/env python3

import sys
import time
import subprocess
import logging
import pyinotify
import datetime as dt

from pathlib import Path

logger = logging.getLogger("watcher")

class Regen(pyinotify.ProcessEvent):

    TIMEOUT = dt.timedelta(seconds=3600)
    SLEEP_TIME = 2.0 # sec

    def my_init(self, trigger:Path, config:Path):
        self.locked = False
        self.trigger = trigger
        self.config = config

    def process_default(self, event):
        logger.debug(f"Caught event {event.maskname} on {self.trigger}")
        if self.locked:
            logger.debug(f"Generator is locked - quit")
            return
        if not self.trigger.exists() or self.trigger.stat().st_size <= 1:
            self.__regen()

    def __regen(self):
        logger.debug("Regenerate called")
        if self.locked:
            logger.debug(f"Regenerate for {self.trigger} already in progress - quit")
            return

        self.locked = True
        try:
            logger.info(f"Regenerating site for trigger {self.trigger}")
            trigger_file = self.trigger.open("wt")
            trigger_file.write(f"Generation started at {dt.datetime.now()}")
            subprocess.call(["pelican", "-s" , self.config], stdout=trigger_file, stderr=trigger_file)
            trigger_file.write(f"Generation ended at {dt.datetime.now()}")
        finally:
            trigger_file.close()
            time.sleep(0.001)
            self.locked = False
        logger.info("Regenerate complete")

def main(app_folder: Path, mode: str):
    if not app_folder.is_dir():
        logger.error(f"{app_folder} does not exist")
        return 1

    config = app_folder / "{mode}conf.py"
    if not config.exists():
        logger.error(f"{config} does not exist")
        return 1

    trigger = app_folder / "content" / f".{mode}"
    if not trigger.exists():
        trigger.touch()

    regen = Regen(config=config, trigger=trigger)

    wm = pyinotify.WatchManager()
    notifier = pyinotify.AsyncNotifier(wm, default_proc_fun=regen, read_freq=2)
    wm.add_watch(
        str(trigger),
        pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY)

    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            print("keyboard Interrupt.")
            notifier.stop()
            break 

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: {} [--preview] [--debug] PATH".format(sys.argv[0]))
        print("  PATH must contain content/ folder and either publishconf.py or .previewconf.py")
        print("       depending on whether --preview was specified")
        sys.exit(1)
    if "--debug" in sys.argv:
        debug = True
        sys.argv.remove("--debug")
    if "--preview" in sys.argv:
        mode = "preview"
        sys.argv.remove("--preview")
    folder = sys.argv[1]
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    sys.exit(main(Path(folder), mode) or 0)
