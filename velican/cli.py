import sys
import getopt
from . import app
from . import utils

APP_PATH = Path("/opt/pelican")

def add(url: str, **kwargs):
	ensure_installed()
	domain, path = utils.split_url(url)
	config_root = app.CONFIG_ROOT / url
	ctx = dict(
		domain=domain,
		path=path,
		output=f'/var/www/{domain}/{utils.to_dirname(path)}',
		content=f'/var/webdav/{domain}/{utils.to_dirname(path)}',
		theme="Peli-Kiera", # "twenty-html5up"
		**kwargs # author, title, subtitle, twitter, linkedin, github, email, address, contact
	)
	config_root.mkdir(parents=True, exist_ok=True)
	render_config("data/conf/pelicanconf.py", config_root / "pelicanconf.py", ctx)
	render_config("data/conf/previewconf.py", config_root / "previewconf.py", ctx)
	render_config("data/conf/publishconf.py", config_root / "publishconf.py", ctx)


def ensure_installed():
	if APP_PATH.exists():
		return
	install()

def install():
	APP_PATH.mkdir(parents=True, exist_ok=True)

	plugins = APP_PATH / "plugins"
	if not plugins.exists():
		utils.log_info(f"Installing plugins by cloning a git repo into {plugins}")
		subprocess.run(["git", "clone", "https://github.com/getpelican/pelican-plugins.git", str(plugins)], check=True)

	themes = APP_PATH / "themes"
	if not themes.exists():
		utils.log_info(f"Installing themes by cloning a git repo into {themes}")
		subprocess.run(["git", "clone", "https://github.com/katomaso/velican-themes.git", str(themes)], check=True)

	utils.log_info("Installation done")


def main():
	"""Usage:
		velican install
		velican add <url> --author=<author> --title=<title> --subtitle=<subtitle>
	"""
	args = os.argv[1:]

	if len(args) == 0:
		print(__doc__)
		return

	command = args.pop(0)
	if command == "add":
		opts, arg = getopt.gnu_getopt(args, [], longopts=["author=", "title=", "subtitle="])
		add(arg[0], **{k.strip("-"): v for k, v in opts})
	elif command == "install":
		install()
	else:
		print(__doc__)