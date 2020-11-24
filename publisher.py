#!/usr/bin/env python3

import sys
import time
import subprocess
import logging
import pyinotify
import datetime as dt
import argparse

from pathlib import Path

logger = logging.getLogger("watcher")

class Regen(pyinotify.ProcessEvent):

    TIMEOUT = dt.timedelta(seconds=3600)
    SLEEP_TIME = 2.0 # sec

    def my_init(self, trigger:Path, config:Path):
        self.locked = False
        self.trigger = config
        self.config = trigger

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

def main(app_folder: Path):
    if not app_folder.is_dir():
        logger.error(f"{app_folder} does not exist")
        return 1

    config = app_folder / "pelicanconf.py"
    if not config.exists():
        logger.error(f"{config} does not exist")
        return 1

    trigger = app_folder / ".publish"
    if not trigger.exists():
        trigger.touch()

    regen = Regen(config=str(config), trigger=str(trigger))

    wm = pyinotify.WatchManager()
    notifier = AsyncNotifier(wm, read_freq=2)
    wm.add_watch(
        str(app_folder / ".publish"),
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
    parser = argparse.ArgumentParser(description='Watch .publish file to trigger site regeneration')
    parser.add_argument('FOLDER', metavar='folder', type=str,
                        help='site root folder')
    parser.add_argument('--debug', dest='debug', action='store_const',
                        default=False)

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    sys.exit(main(Path(args.folder)) or 0)
