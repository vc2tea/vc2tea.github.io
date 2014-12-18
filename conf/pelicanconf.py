#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = '綠茶'
SITENAME = '綠茶如是说'
SITESUBTITLE = '我们走得太快，灵魂都跟不上了'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Hong_Kong'

DEFAULT_LANG = 'zh'

DATE_FORMATS = {
    'zh': '%Y-%m-%d(%a)',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/vc2tea'),)

DEFAULT_PAGINATION = 5

STATIC_PATHS = [
    'static',
]

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

THEME = "pelican-bootstrap3"
DEFAULT_CATEGORY = 'Blog'
DISPLAY_CATEGORIES_ON_MENU = False
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = (".git","CNAME","conf","bak")

ARTICLE_URL = '{slug}'
ARTICLE_SAVE_AS = '{slug}.html'
PAGE_URL = 'pages/{slug}'
PAGE_SAVE_AS = 'pages/{slug}.html'
AUTHOR_URL = 'author/{slug}'
AUTHOR_SAVE_AS = 'author/{slug}.html'
CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}.html'
TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}.html'