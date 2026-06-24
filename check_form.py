import urllib.request
import re

opener = urllib.request.build_opener()
resp = opener.open('http://127.0.0.1:5000/auth/login')
html = resp.read().decode('utf-8')

# Find form section
form_start = html.find('<form')
form_end = html.find('</form>') + 7
if form_start != -1:
    form_html = html[form_start:form_end]
    print('Form HTML:')
    print(form_html)
else:
    print('Form not found')
    print(f'\nPage contains: <form: {"<form" in html}')
    print(f'Page contains: csrf_token: {"csrf_token" in html}')
