import acme_tiny
import subprocess
import jinja2
import shutil
import pkg_resources
from datetime import date

ACME_URL = acme_tiny.DEFAULT_DIRECTORY_URL
ACME_KEY = "/etc/ssl/acme/account.key"
ACME_CHALLENGE = "/var/www/.well-known/acme-challenge"

def exist_domain(domain: str) -> bool :
	crt_link = f"/etc/ssl/private/{domain}.crt"
	domain_conf = f"/etc/nginx/conf.d/{domain}.conf"
	return os.exists(crt_link) and os.exists(domain_conf)

def add_domain(domain: str):
	"""Create nginx conf and domain certificate and systemd renewal timer""" 
	if domain.startswith("http"):
		raise ValueError("Domain must not contain schema (http[s])")
	if "/" in domain:
		raise ValueError("Domain must not contain path")

	assert os.exists(ACME_KEY)
	assert os.isdir(ACME_CHALLENGE)

	d = date.today()
	key = f"/etc/ssl/acme/{domain}.key"
	csr = f"/etc/ssl/acme/{domain}.csr"
	crt = f"/etc/ssl/acme/{domain}-{d.year}{d.month}{d.day}.crt"
	crt_link = f"/etc/ssl/private/{domain}.crt"

	# create private key for the domain
	with open(key, "wb") as key_file:
		subprocess.run(["openssl", "genrsa", "4096"], stdout=key_file, check=True, capture_output=True)

	# create a CSR for the domain
	with open(csr, "wb") as csr_file:
		subprocess.run(["openssl", 'req', '-new', '-sha256', '-key', key, '-subj', f'"/CN={domain}"'], stdout=csr_file, check=True, capture_output=True)

	domain_folder = f"/etc/nginx/conf.d/{domain}"
	os.mkdir(domain_folder)
	utils.render_resource("conf/nginx.conf", f"/etc/nginx/conf.d/{domain}.conf", {
		"DOMAIN_CRT": crt, "DOMAIN_KEY": key, "DOMAIN": domain})

	# add domain renewal timer and start it right away
	if not os.exists(SYSTEMD_TEMPLATE):
		# install the template for certificate renewals
		utils.render_resource("conf/systemd.template", SYSTEMD_TEMPLATE, {
			"binary": shutil.which("velican")}) # installed as entry-point

	utils.render_resource("conf/systemd.timer", f"/etc/systemd/system/renew-domain@{domain}.timer", {})

	subprocess.run(["systemctl", "enable", f"renew-domain@{domain}.timer"], check=True, capture_output=True)
	subprocess.run(["systemctl", "start", f"renew-domain@{domain}.timer"], check=True, capture_output=True)


def	renew_domain(domain: str):
	crt = f"/etc/ssl/acme/{domain}-{d.year}{d.month}{d.day}.crt"
	crt_link = f"/etc/ssl/private/{domain}.crt"
	
	if os.exists(crt_link):
		crt_prev = os.path.realpath(crt_link)

	# sign the request using acme_tiny
	crt_data = acme_tiny.sign(csr=csr, acme_dir=ACME_CHALLENGE, account_key=ACME_KEY)
	with open(crt, "wb") as crt_file:
		crt_file.write(crt_data)

	subprocess.run(["nginx", "-t"], check=True)
	subprocess.run(["systemctl", "reload", "nginx"], check=True)