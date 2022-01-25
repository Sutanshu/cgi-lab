#!/usr/bin/env python3

import cgi, cgitb

cgitb.enable()

from templates import login_page, secret_page, after_login_incorrect
import secret, os
from http.cookies import SimpleCookie

s = cgi.FieldStorage()
username, password = s.getfirst("username"), s.getfirst("password")

form_ok = username == secret.username and password == secret.password

cookie = SimpleCookie(os.environ["HTTP_COOKIE"])
cookie_un = None
cookie_pw = None

if cookie.get("username"):
    cookie_un = cookie.get("username").value
if cookie.get("password"):
    cookie_pw = cookie.get("password").value

cookie_ok = cookie_un == secret.username and cookie_pw == secret.password

if cookie_ok:
    username = cookie_un
    password = cookie_pw
print("Content-Type: text/html")
if form_ok:
    print(f"Set-Cookie: username={username}")
    print(f"Set-Cookie: password={password}")

print()

if not (username and password):
    print(login_page())
elif username == secret.username and password == secret.password:
    print(secret_page(username, password))
else:
    print(login_page())
    print(f"Hello {username} your password is {password}")
