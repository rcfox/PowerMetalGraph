# Try not to run this script too often. It pulls down a couple MB of text from Wikipedia.

import requests
import re
import urllib

list_url = 'http://en.wikipedia.org/w/api.php?format=json&action=query&titles=List_of_power_metal_bands&prop=revisions&rvprop=content&continue='

r = requests.get(list_url)
list_json = r.json()

pages = list_json['query']['pages']
content = pages.values()[0]['revisions'][0]['*']
links = []
for m in re.finditer(r'\n\s*\|\s*\[\[(.+?)\]\]', content):
    inner = m.group(1).split('|')
    link = inner[0]
    if len(inner) > 1:
        band_name = inner[1]
    else:
        band_name = inner[0]
    links.append(urllib.quote_plus(link.encode('utf-8')))

segment_size = 50
for i in xrange(0, len(links), segment_size):
    segment = links[i : i + segment_size]
    new_url = 'http://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&continue=&titles=' + '|'.join(segment)
    r = requests.get(new_url)
    pages_json = r.json()
    pages = {page_id: page_text['revisions'][0]['*'] for page_id, page_text in pages_json['query']['pages'].items()}
    for page_id, page_text in pages.items():
        m = re.match(r'#REDIRECT \[\[(.+?)\]\]', page_text)
        if m:
            print '%s is a redirect!' % page_id
            links.append(m.group(1))
            continue
        
        with open('%s.txt' % page_id, 'w') as f:
            print page_id
            f.write(page_text.encode('utf-8'))
            
