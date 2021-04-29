import sys
import getopt
import subprocess
from . import PELICAN_ROOT, CONFIG_ROOT
from . import utils


def add(url: str, **kwargs):
	ensure_installed()
	domain, path = utils.split_url(url)
	config_root = CONFIG_ROOT / url
	ctx = dict(
		domain=domain,
		path=path,
		output=f'/var/www/{domain}/{utils.to_dirname(path)}',
		content=f'/var/webdav/{domain}/{utils.to_dirname(path)}',
		theme="Peli-Kiera", # "twenty-html5up"
		**kwargs # author, title, subtitle, twitter, linkedin, github, email, address, contact
	)
	config_root.mkdir(parents=True, exist_ok=True) # good for update but bad for security...
	render_config("data/conf/pelicanconf.py", config_root / "pelicanconf.py", ctx)
	render_config("data/conf/previewconf.py", config_root / "previewconf.py", ctx)
	render_config("data/conf/publishconf.py", config_root / "publishconf.py", ctx)


def ensure_installed():
	if PELICAN_ROOT.exists():
		return
	install()

def install():
	PELICAN_ROOT.mkdir(parents=True, exist_ok=True)

	plugins = PELICAN_ROOT / "plugins"
	if not plugins.exists():
		utils.log_info(f"Installing plugins by cloning a git repo into {plugins}")
		subprocess.run(["git", "clone", "https://github.com/getpelican/pelican-plugins.git", str(plugins)], check=True)

	themes = PELICAN_ROOT / "themes"
	if not themes.exists():
		utils.log_info(f"Installing themes by cloning a git repo into {themes}")
		subprocess.run(["git", "clone", "https://github.com/katomaso/velican-themes.git", str(themes)], check=True)

	utils.log_info("Installation done")


def main():
	"""Usage:
    velican install
    velican add <url> --author=<author> --title=<title> --subtitle=<subtitle>
	"""
	args = sys.argv[1:]

	if len(args) == 0:
		print(main.__doc__)
		return

	command = args.pop(0)
	if command == "add":
		opts, arg = getopt.gnu_getopt(args, [], longopts=["author=", "title=", "subtitle="])
		add(arg[0], **{k.strip("-"): v for k, v in opts})
	elif command == "install":
		install()
	else:
		print(main.__doc__)