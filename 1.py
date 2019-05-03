import requests
r = requests.get('http://www.google.com/')
print(r.content)