from pathlib import Path

# port on which the velican app listens
PORT = 9180

# output_root contains logs resp. locks with suffixes .log resp. .lock.
# lock contains timestamp of the start of the operation and has a timeout
OUTPUT_ROOT = Path("/var/velican/")

# config_root is the directory for configurations for each blog/site organized
# by full URLs (domain + path)
CONFIG_ROOT = Path("/opt/velican/")

# pelican_root is the place for all pelican additions
PELICAN_ROOT = Path("/opt/pelican/")

# Systemd root to install service to
SYSTEMD_ROOT = Path("/etc/systemd/system/")