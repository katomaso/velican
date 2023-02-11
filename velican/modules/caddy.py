import requests

from sqlalchemy import event
from models import Blog

def register_domain_to_caddy():
    """Let caddy know about new routing"""
    requests.post("caddy-admin:9900", {"route": ...})

def init(caddy_url: str):
    event.listen(Blog, "before_insert", register_domain_to_caddy, propagate=True)
