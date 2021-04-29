from pathlib import Path

# output_root contains logs resp. locks with suffixes .log resp. .lock.
# lock contains timestamp of the start of the operation and has a timeout
OUTPUT_ROOT = Path("/var/velican/")

# config_root is the directory for configurations for each blog/site organized
# by full URLs (domain + path)
CONFIG_ROOT = Path("/srv/velican/")

# pelican_root is the place for all pelican additions
PELICAN_ROOT = Path("/opt/pelican")