import os.path
import configparser

DELETE_OUTPUT_DIRECTORY = True
CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True

DISPLAY_PAGES_ON_MENU = True

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = '{{lang|default("cs_CZ")}}'
LOCALE = 'en_US.UTF-8'

USE_FOLDER_AS_CATEGORY = True
# content path
PATH = '{{content}}'
STATIC_PATHS = ('static', 'images')

ARTICLE_SAVE_AS = '{category}/{slug}.html'
ARTICLE_URL = '{category}/{slug}.html'

THEME="{{theme_root}}/{{theme}}"

# plugins are shared for all pelican instances
PLUGIN_PATHS = ['{{plugin_root}}', '{{plugin_root}}/neighbors/pelican/plugins']
PLUGINS = ['neighbors', 'pelican-readtime']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
FEED_ALL_RSS = 'feeds/rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 30
LAST_ARTICLE_COUNT = 9

MENUITEMS = [
   # ("title", "url"),
]

# Template variables
this_dir = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(this_dir + "/config.ini")
for key, value in config.items('context'):
	locals()[key.upper()] = value

if 'SUBTITLE' in locals():
	SITESUBTITLE = SUBTITLE

if 'TITLE' in locals():
	SITENAME = TITLE

SOCIAL = []

if 'TWITTER' in locals():
    SOCIAL.append(('twitter', 'https://twitter.com/{{TWITTER}}'))
if 'LINKEDIN' in locals():
    SOCIAL.append(('linkedin', 'https://linkedin.com/in/{{LINKEDIN}}'))
if 'GITHUB' in locals():
    SOCIAL.append(('github', 'https://github.com/{{GITHUB}}'))

COPYRIGHT = AUTHOR