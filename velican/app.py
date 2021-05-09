import subprocess
import threading
import datetime as dt

from . import OUTPUT_ROOT, CONFIG_ROOT, CONTENT_ROOT
from . import utils
from flask import Flask, request

LOCK_TIMEOUT = 60 # seconds
global_lock = set()

app = Flask("velican")

@app.route('/<path:path>', methods=['POST', 'GET'])
def handle(path):
	if path.endswith(".publish"):
		command = "publish"
		path = path[:-len("/.publish")]
	elif path.endswith(".preview"):
		command = "preview"
		path = path[:-len("/.preview")]
	else:
		return "", 404

	if not _lock(request):
		return "", 202
	
	output_path = OUTPUT_ROOT / request.host / path / command
	config_path = CONFIG_ROOT / request.host / path / (command + "conf.py")
	if not config_path.exists():
		output_path = (OUTPUT_ROOT / request.host / path).parent / command
		config_path = (CONFIG_ROOT / request.host / path).parent / (command + "conf.py")
		if not config_path.exists():
			return f"Missing {command}conf.py\r\n", 500
	try:
		if not output_path.exists():
			output_path.parent.mkdir(exist_ok=True, parents=True)
			output_path.touch()

		if not config_path.exists():
			return f"Missing {config_path}\r\n", 500
		if request.method == "GET":
			return status(output_path), 200
		elif request.method == "POST":
			return regen(output_path, config_path), 201
	finally:
		_unlock(request)


def regen(output_path, config_path) -> tuple[str, int]:
	# create a file based lock
	lock_path = output_path.with_suffix(".lock")
	log_path = output_path.with_suffix(".log")
	def _regen():
		# create a file based lock, not to generate multiple times within one minute
		now = dt.datetime.now()
		if lock_path.exists():
			ts = dt.datetime.fromisoformat(lock_path.read_text())
			if (now - ts) < dt.timedelta(minutes=1):
				return
		try:
			lock_path.write_text(now.isoformat())
			with log_path.open("wt") as log_file:
				subprocess.call(["pelican", "-s" , str(config_path)], stdout=log_file, stderr=log_file)
		finally:
			lock_path.unlink()
	# blog generating process does not block the response to the client
	t = threading.Thread(target=_regen)
	t.daemon = True
	t.start()
	return ""


def status(output_path) -> tuple[str, int]:
	"""status will return
	- either 200 if regen was completed together with complete log
	- or 202 (Accepted) with partial log of the regen operation
	"""
	log_path = output_path.with_suffix(".log")
	if log_path.exists():
		return log_path.read_text()
	return ""


def _lock(request) -> bool:
	"""Get the lock for a long-running operation"""
	lock_key = request.host + request.script_root
	if lock_key in global_lock:
		return False
	global_lock.add(lock_key)
	return True


def _unlock(request):
	"""Get the lock for a long-running operation"""
	lock_key = request.host + request.script_root
	global_lock.remove(lock_key)
