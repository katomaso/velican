import configparser
import getopt
import ngm2
import random
import string
import subprocess
import sys
from . import PELICAN_ROOT, CONFIG_ROOT, SYSTEMD_ROOT, PORT
from . import utils

def create(url: str, theme: str, password: str, username="admin", **kwargs):
	domain, path = utils.split_url(url)
	config_root = CONFIG_ROOT / url
	config_root.mkdir(parents=True, exist_ok=True) # good for update but bad for security
	ctx_file_path = config_root / 'config.ini'
	ctx_file = configparser.ConfigParser()
	if ctx_file_path.exists():
		ctx_file.read(ctx_file_path)
	if not password:
		password = "".join(random.sample(string.ascii_letters + string.digits, 8))
	ngm2.add_auth(username, password, url)
	ctx = dict(
		url=url,
		domain=domain,
		path=path,
		theme=theme, # "twenty-html5up"
		theme_root=PELICAN_ROOT / "themes",
		plugin_root=PELICAN_ROOT / "plugins",
		output=ngm2.add_html(url),
		content=ngm2.add_webdav(url + "/webdav", auth=url),
	)
	ctx_file['server'] = ctx
	with open(config_root / 'config.ini', 'w') as configfile:
		ctx_file.write(configfile)
	# finish nginx configuration
	ngm2.add_proxy(f"{url}/.publish", PORT, auth=url)
	ngm2.add_proxy(f"{url}/.preview", PORT, auth=url)
	ngm2.apply()

	utils.render_resource("conf/pelicanconf.py", config_root / "pelicanconf.py", ctx)
	utils.render_resource("conf/previewconf.py", config_root / "previewconf.py", ctx)
	utils.render_resource("conf/publishconf.py", config_root / "publishconf.py", ctx)
	return password

def update(url: str, ctx: dict):
	"""Update blog's context configuration"""
	ctx_file = configparser.ConfigParser()
	ctx_file.read(config_root / 'config.ini')
	ctx_file['context'].update(**ctx)
	with open(config_root / 'config.ini', 'w') as configfile:
		config.write(configfile)

def ensure_installed():
	if PELICAN_ROOT.exists():
		return
	install()

def install():
	PELICAN_ROOT.mkdir(parents=True, exist_ok=True)

	plugins = PELICAN_ROOT / "plugins"
	if not plugins.exists():
		utils.log_info(f"Installing plugins by cloning a git repo into {plugins}")
		subprocess.run(["git", "clone", "--recurse-submodules", "https://github.com/katomaso/velican-plugins.git", str(plugins)], check=True)
	else:
		utils.log_info(f"Updating plugins in {plugins}")
		subprocess.run(["git", "pull", "--recurse-submodules"], cwd=str(plugins), check=True)

	themes = PELICAN_ROOT / "themes"
	if not themes.exists():
		utils.log_info(f"Installing themes by cloning a git repo into {themes}")
		subprocess.run(["git", "clone", "--recurse-submodules", "https://github.com/katomaso/velican-themes.git", str(themes)], check=True)
	else:
		utils.log_info(f"Updating themes in {themes}")
		subprocess.run(["git", "pull", "--recurse-submodules"], cwd=str(themes), check=True)

	service = SYSTEMD_ROOT / "velican.service"
	if not service.exists():
		utils.log_info("Installing systemd service")
		utils.render_resource("conf/systemd.service", service, {"port": PORT})
		subprocess.run(["systemctl", "enable", "velican"], check=True)
		subprocess.run(["systemctl", "start", "velican"], check=True)

	utils.log_info("Installation done")


def main():
	"""Usage:
    velican themes
    velican create <url> [--theme] [--username] [--password]
    velican update <url> OPTIONS
    valican upgrade
    """
	args = sys.argv[1:]
	utils.log_level("info")

	if len(args) == 0:
		print(main.__doc__)
		return

	ensure_installed()

	command = args.pop(0)
	if command == "create":
		opts, arg = getopt.gnu_getopt(args, "", longopts=["theme=", "username="])
		if "--password" not in opts:
			opts["--password"] = input("Password: ")
		create(url=arg[0], **{k.strip("-"): v for k, v in opts})
	elif command == "update":
		opts, arg = getopt.gnu_getopt(args, "", longopts=["author=", "sitename=", "sitesubtitle=", "twitter=", "linkedin=", "github=", "facebook=", "instagram="])
		update(arg[0], **{k.strip("-").upper(): v for k, v in opts})
	elif command == "themes":
		for theme in (PELICAN_ROOT / "themes").iterdir():
			print(theme)
	elif command == "upgrade":
		install()
	else:
		print(main.__doc__)