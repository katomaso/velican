# Flow:
#  - user creates an account in Authelia/Keyclock....
#  - 

("/account", "POST", account_create, "create a new account"),
("/account", "GET", account_get, "account summary (managed domains etc)"),
("/theme", "GET,POST,DELETE", theme, "manage available themes"),
("/plugin", "GET,POST,DELETE", theme, "manage available plugins"),
("/domain", "GET", domain_add, "list domains assigned to the account (HTML: offer to create a new one)"),
("/domain", "POST", domain_add, "assign a domain to an account"),
("/domain/<domain>/article/<article>", "GET,POST,DELETE", article, "update metadata and content of an article"),
("/domain/<domain>/publish", "POST", domain_publish, "generate HTML output to production folder"),
("/domain/<domain>/preview", "POST", domain_preview, "generate HTML output to staging folder"),



def domain_add(domain: str, path="": str):
    user = request.headers.remote_user
    if not user:
        raise http401("Unauthorized")

    name = request.headers.remote_name
    groups = request.headers.remote_groups
    email = request.headers.remote_email
    ROOT = os.path.join(content_root, domain)
    os.path.mkdir(f'{root}')
    os.path.mkdir(f'{root}/content')
    os.path.mkdir(f'{root}/production')
    os.path.mkdir(f'{root}/staging')
    render("pelicanconf.py", root, {domain: str})



domain_settings = {
    "domain": "example.com",
    "theme": "default",
    "lang": "cs_CZ",
    "timezone": "Europe/Prague",
    "title": "",
    "subtitle": "",
    "twitter": "",
    "facebook": "",
    "linkedin": "",
    "github": "",
    "instagram": "",
    "tiktok": "",
    "user": "",
}