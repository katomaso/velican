#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.
import os
import sys

from .pelicanconf import *

SITEURL = "https://{{domain}}{{path}}/preview/"
OUTPUT_PATH="{{output}}/preview"

# Following items are often useful when publishing
DISQUS_SITENAME = "{{domain|safe}}{{path|safe}}-preview"
