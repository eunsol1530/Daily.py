import requests
import re

# Get Url
url = input('Enter a URL (include `http://` or `https://`): ')

# Ensure the URL uses HTTPS
if url.startswith('http://'):
    print("Warning: Switching to HTTPS for secure communication.")
    url = url.replace('http://', 'https://', 1)

# Connect
website = requests.get(url)

# Read
html = website.text

# Grab Links
links = re.findall('"((http|ftp)s?://.*?)"', html)

# Output Links
for link in links:
    print(link[0])