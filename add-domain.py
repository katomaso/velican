#!/usr/bin/env python3

import acme_tiny
import subprocess
import jinja2
from datetime import date

ACME_KEY = "/etc/ssl/acme/account.key"
ACME_CHALLENGE = "/var/www/.well-known/acme-challenge"

def add_domain(domain: str):
	assert "/" not in domain # sanity check
	assert os.exists(ACME_KEY)
	assert os.isdir(ACME_CHALLENGE)

	d = date.today()
	key = f"/etc/ssl/acme/{domain}.key"
	csr = f"/etc/ssl/acme/{domain}.csr"
	crt = f"/etc/ssl/acme/{domain}-{d.year}{d.month}{d.day}.crt"
	crt_link = f"/etc/ssl/private/{domain}.crt"

	# create private key for the domain
	with open(key, "wb") as key_file:
		subprocess.run(["openssl", "genrsa", "4096"], stdout=key_file, check=True)

	# create a CSR for the domain
	with open(csr, "wb") as csr_file:
		subprocess.run(["openssl", 'req', '-new', '-sha256', '-key', key, '-subj', f'"/CN={domain}"'], stdout=csr_file, check=True)

	# sign the request using acme_tiny
	crt_data = acme_tiny.sign(csr=csr, acme_dir=ACME_CHALLENGE, account_key=ACME_KEY)
	with open(crt, "wb") as crt_file:
		crt_file.write(crt_data)

	nginx_conf = f"/etc/nginx/sites-enabled/{domain}"
	nginx_conf_content = jinja2.Template("conf/nginx.conf").render(
		{"DOMAIN_CRT": crt, "DOMAIN_KEY": key, "DOMAIN": domain})
	with open(nginx_conf, "wt") as nginx_conf_file:
		nginx_conf_file.write(nginx_conf_content)

	subprocess.run(["nginx", "-t"], check=True)
	subprocess.run(["systemctl", "reload", "nginx"], check=True)

	# create web roots
	os.mkdir(f"/var/www/{domain}") # throws if folder already exists
	os.mkdir(f"/var/webdav/{domain}") # throws if folder already exists


def	renew_domain(domain: str):
	crt_last = os.path.realpath(f"/etc/ssl/private/{domain}.crt")