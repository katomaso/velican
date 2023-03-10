from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# port on which the velican app listens
PORT = 9180

# output_root contains logs resp. locks with suffixes .log resp. .lock.
# lock contains timestamp of the start of the operation and has a timeout
OUTPUT_ROOT = Path("/var/www/")
SOURCE_ROOT = Path("/var/velican/")

# pelican_root is the place for all pelican additions
PELICAN_ROOT = Path("/opt/pelican/")

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://velican:velican@localhost:5432/dbname'
SQLALCHEMY_DATABASE_URI = 'sqlite:///velican.db'

SERVER_MODULE = None  # choices: caddy ...

FACEBOOK_ID = 'facebook app id',
FACEBOOK_SECRET = 'facebook app secret'

SECURITY_POST_LOGIN = '/profile'