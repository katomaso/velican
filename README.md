# Velikan

Velikan is professional blogging software that does not require backend. It usesonly HTTP and WebDAV
protocols implemented by your favorite web server. Rendering and logic is implemented in javascript
that is served to clients. Your blog is unhackable and extremely easy on your server.

## How does it work?

Velikan uses WebDAV protocol for writing files to the server. WebDAV is amazing standardized protocol
that is implemented by all mainline webservers. It works pretty much like Dropbox or Google Drive.

By default, posts are simply markdown files in folders. One folder (and all its subfolders) is accessible
by your webserver - this is your "publish" folder. To store your drafts, velican uses a different folder
that is not accessible by HTTP but only by WebDAV. Publishing is then done by moving the files between
folders.

Depending on your folder structure, blog can support categories and even language mutations. It requires
extra work in managing folder but hey, no free lunches.

## Security

If you use HTTPS then your only security concert is securing your WebDAV endpoint. Because of encrypted
traffic, you can use basic authorization provided by your favorite webserver. Accounts can be stored in
httpasswd file or some webservers even support integration with LDAP. 

## Extensibility

Any additional functionality of your blog can be done only in javascript using microservices. Comments,
for example, can be added via Disqus.
