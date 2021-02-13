#!/usr/bin/env python3

import acme_tiny
import subprocess
import jinja2
import shutil
import pkg_resources
from datetime import date

SYSTEMD_TEMPLATE = "/etc/systemd/system/renew-domain@.service"

def add_blog(url: str):
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

	# if not exist_webdav(domain, path):
	# 	add_webdav(domain, path, user, password)

def add_path(domain: str, path: str):
	"""Add nginx "location" configuration into domain's conf.d folder"""
	path_safe_name = path[1:].replace('/', '-') if path != "/" else "default"
	nginx_path = f"/etc/nginx/conf.d/{domain}/{path_safe_name}.conf"
	nginx_path_content = jinja2.Template(pkg_resources.resource_string("velican", "conf/nginx.path")).render(
		{"path": path, "path_safe_name": path_safe_name, "domain": domain})
	with open(SYSTEMD_TEMPLATE, "wt") as nginx_path_file:
		nginx_path_file.write(nginx_path_content)

	# create web roots
	os.makedirs(f"/var/www/{domain}{path}") # throws if folder already exists
	shutil.chown(f"/var/www/{domain}{path}", "www-data")

	subprocess.run(["nginx", "-t"], check=True)
	subprocess.run(["systemctl", "reload", "nginx"], check=True)

# def add_webdav(domain: str, path: str, user: str, password: str):
# 	os.makedirs(f"/var/webdav/{domain}{path}") # throws if folder already exists
# 	shutil.chown(f"/var/webdav/{domain}{path}", "www-data")