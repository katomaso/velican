#!/usr/bin/env python3

import subprocess
import shutil
from datetime import date

from . import utils

SYSTEMD_TEMPLATE = "/etc/systemd/system/renew-domain@.service"

def add_blog(url: str, username: str, password: str):
	print(local)
	return
	domain = url
	path = ""
	if "/" in url:
		domain, path = domain.split("/", 1)
	path = "/" + path

	if not exist_domain(domain):
		add_domain(domain)

	if not exist_path(domain, path):
		add_path(domain, path)

	if not exist_webdav(domain, path):
		add_webdav(domain, path, username, password)

def add_path(domain: str, path: str):
	"""Add nginx "location" configuration into domain's conf.d folder"""
	path_safe_name = path[1:].replace('/', '-') if path != "/" else "default"
	utils.rener_resource("conf/nginx.path", f"/etc/nginx/conf.d/{domain}/{path_safe_name}.conf", {
		"path": path, "path_safe_name": path_safe_name, "domain": domain
		}
	)
	# create web roots
	os.makedirs(f"/var/www/{domain}{path}") # throws if folder already exists
	shutil.chown(f"/var/www/{domain}{path}", "www-data")

	subprocess.run(["nginx", "-t"], check=True)
	subprocess.run(["systemctl", "reload", "nginx"], check=True)

def add_webdav(domain: str, path: str, username: str, password: str):
	"""Add nginx "location" configuration into domain's conf.d folder"""
	path_safe_name = (path[1:].replace('/', '-') if path != "/" else "default") + "-webdav"
	authfile = f"/var/webdav/.{{domain}}-{{path_safe_name}}.htpasswd"

	pwfile = htpasswd.HtpasswdFile(authfile, create=htpasswd.options.create)
	pwdfile.update(username, password)
	pwfile.save()

	os.makedirs(f"/var/webdav/{domain}{path}") # throws if folder already exists
	shutil.chown(f"/var/webdav/{domain}{path}", "www-data")

	utils.rener_resource("conf/nginx.webdav", f"/etc/nginx/conf.d/{domain}/{path_safe_name}.conf", {
		"path": path, "path_safe_name": path_safe_name, "domain": domain, "authfile": authfile}
	)
