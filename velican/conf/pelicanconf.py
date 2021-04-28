#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os.path

AUTHOR = '{{name}}'
TITLE = '{{title}}'
SUBTITLE = '{{subtitle}}'

SITEURL = 'https://{{domain}}{{path}}'
ADDRESS = "Prague, Czechia"
MAIL = EMAIL = "{{email}}"
CONTACT = "{{contact}}"

TWITTER = '{{twitter}}'
LINKEDIN = '{{linkedin}}'
GITHUB = '{{github}}'

DELETE_OUTPUT_DIRECTORY = True
CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True

DISPLAY_PAGES_ON_MENU = True

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = '{{lang}}'
LOCALE = 'en_GB.UTF-8'

USE_FOLDER_AS_CATEGORY = True
# content path
PATH = '{{content}}'
STATIC_PATHS = ('static', 'images')

ARTICLE_SAVE_AS = '{category}/{slug}.html'
ARTICLE_URL = '{category}/{slug}.html'

THEME="/opt/pelican/themes/{{theme}}"

# plugins are shared for all pelican instances
PLUGIN_PATHS = ['/opt/pelican/plugins']
PLUGINS = ['readtime', 'neighbors']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
FEED_ALL_RSS = 'feeds/rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = [
   # ("Resume", "author/tomas-peterka.html"),
]

# Template variables
NAME = AUTHOR
TAGLINE = SITESUBTITLE = SUBTITLE
SITENAME = TITLE

SOCIAL = []

if TWITTER:
    social.append(('twitter', 'https://twitter.com/{{TWITTER}}'))
if LINKEDIN:
    social.append(('linkedin', 'https://linkedin.com/in/{{LINKEDIN}}'))
if GITHUB:
    social.append(('github', 'https://github.com/{{GITHUB}}'))

COPYRIGHT = AUTHOR
DEFAULT_PAGINATION = 30
LAST_ARTICLE_COUNT = 9

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

{{extra}}