#!/usr/bin/env python
# -*- coding: utf-8 -*- #
# AUTHOR = 'Adrien Oyono'
SITENAME = 'Morning Dew'
SITEURL = 'http://localhost:8000'

PATH = 'content'
PAGE_PATHS = ['pages']
PLUGIN_PATHS = ['plugins', 'plugins/pelican-plugins', '../pelican-themes/']
PLUGINS = ['pelican-ert',]

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (
    ('<span class="fab fa-linkedin"></span> Linkedin', 'https://www.linkedin.com/in/adrienoyono'),
    ('<span class="fab fa-facebook"></span> Facebook', 'https://www.facebook.com/oyono.owono'),
    ('<span class="fab fa-twitter"></span> Twitter', 'https://twitter.com/onoyoyono'),
    ('<span class="fab fa-github"></span> Github', 'https://github.com/aoyono'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Disable caching
LOAD_CONTENT_CACHE = False

# DELETE_OUTPUT_DIRECTORY = True
DEFAULT_CATEGORY = 'misc'
TYPOGRIFY = True

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_LANG_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/{lang}/'
ARTICLE_LANG_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}/index.html'

PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
PAGE_LANG_URL = 'pages/{slug}/{lang}/'
PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}/index.html'

DRAFT_URL = 'drafts/{slug}/'
DRAFT_SAVE_AS = 'drafts/{slug}/index.html'
DRAFT_LANG_URL = 'drafts/{slug}/{lang}/'
DRAFT_LANG_SAVE_AS = 'drafts/{slug}-{lang}/index.html'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORY_LANG_URL = 'category/{slug}/{lang}/'
CATEGORY_LANG_SAVE_AS = 'category/{slug}-{lang}/index.html'

DEFAULT_DATE = 'fs'

THEME = './theme/'
SITESUBTITLE = "An african's mind"

DISPLAY_PAGES_ON_MENU = True
DELETE_OUTPUT_DIRECTORY = True

# DIRECT_TEMPLATES = ('index', 'categories', 'archives')

COPYRIGHT = "© Copyright 2018, Adrien Oyono"
