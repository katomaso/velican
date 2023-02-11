import os.path
import configparser

DELETE_OUTPUT_DIRECTORY = True
CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True

DISPLAY_PAGES_ON_MENU = True

TIMEZONE = '{{tz|default("Europe/Paris")}}'
DEFAULT_LANG = '{{lang|default("cs_CZ")}}'
LOCALE = '{{lang|default("cs_CZ")}}.UTF-8'

USE_FOLDER_AS_CATEGORY = True
# content path
PATH = '{{content}}'
STATIC_PATHS = ('static', 'images')

ARTICLE_SAVE_AS = '{category}/{slug}.html'
ARTICLE_URL = '{category}/{slug}.html'

THEME="{{theme_root}}/{{theme}}"

# plugins are shared for all pelican instances
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

if 'SUBTITLE' in locals():
	SITESUBTITLE = SUBTITLE

if 'TITLE' in locals():
	SITENAME = TITLE

SOCIAL = []

{% if twitter %}
SOCIAL.append(('twitter', 'https://twitter.com/' + '{{twitter}}'.strip("@")))
{% endif %}
{% if linkedin %}
SOCIAL.append(('linkedin', 'https://linkedin.com/in/' + '{{linkedin}}'.strip("@")))
{% endif %}
{% if github %}
SOCIAL.append(('github', 'https://github.com/' + '{{github}}'.strip("@")))
{% endif %}
{% if instagram %}
SOCIAL.append(('instagram', 'https://instagram.com/'+ '{{instagram}}'.strip("@")))
{% endif %}

COPYRIGHT = AUTHOR