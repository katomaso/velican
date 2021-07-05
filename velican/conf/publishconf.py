import os.path
import sys

sys.path.append(os.path.dirname(__file__))
from pelicanconf import *

SITEURL = "https://{{url}}"
OUTPUT_PATH="{{output}}"

# Following items are often useful when publishing
DISQUS_SITENAME = "{{domain|safe}}{{path|safe}}"
