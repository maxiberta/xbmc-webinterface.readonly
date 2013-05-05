HTML_PATH = '/net/openwrt/mnt/sda1/shared/movies/'

REQ_DATA = '''{"jsonrpc": "2.0",
               "method": "VideoLibrary.GetMovies",
               "params": {"properties" : ["originaltitle", "year", "file", "thumbnail"],
                          "sort": {"order": "ascending", "method": "title"}
                       },
               "id": 1}'''

html = '''<html>
  <head>
    <style type="text/css">
      body {font-family:Arial,Verdana,sans-serif; font-size:12px; font-weight:700; text-align:center;}
      img {box-shadow: 2px 2px 12px grey; margin: 4px 0;}
      .movie {float:left; width:130px; height:220px; vertical-align:top; padding:16px;}
      p {display:inline; overflow:hidden; margin:4px;}
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
    <script src="jquery.lazyload.min.js"></script>
    <script type="text/javascript" charset="utf-8">
      $(function() { $("img").lazyload({effect: "fadeIn"}); });
    </script>
  </head>
  <body>
    % for movie in movies:
    %   if 'file' in movie and movie['file']:
    <div class="movie">
      <a href="${movie['file']}">
      <div>
        <img src="https://raw.github.com/tuupola/jquery_lazyload/1.9.x/img/grey.gif" data-original="${movie['thumbnail']}" width="130" height="190">
      </div>
      <p>${movie['originaltitle']} (${movie['year']})</p>
      </a>
      % if 'subs' in movie and movie['subs']:
      - <a href="${movie['subs']}">(subs)</a>
      % endif
    </div>
    %   endif
    % endfor
  </body>
</html>'''

import os
import urllib
try:
    import xbmc
    print 'EXECUTING JSONRPC QUERY VIA XBMC'
    response = xbmc.executeJSONRPC(REQ_DATA)
except ImportError:
    import requests
    print 'EXECUTING JSONRPC QUERY VIA REQUESTS'
    response = requests.post('http://raspbmc.local/jsonrpc', data=REQ_DATA, headers={'content-type': 'application/json'})
    movies = response.json()['result']['movies']

print 'FOUND %s MOVIES...' % len(movies)
print 'PROCESSING DATA... '
for movie in movies:
    movie['thumbnail'] = urllib.unquote(movie['thumbnail'])
    if movie['thumbnail'].startswith('image://'):
        movie['thumbnail'] = movie['thumbnail'][8:]

print 'LOADING MAKO...'
from mako.template import Template
print 'RENDERING TEMPLATE...'
template = Template(html, output_encoding='utf-8', encoding_errors='replace')
out = template.render(movies=movies)
with open(os.path.join(HTML_PATH, 'index.html'), 'w') as index_html:
    index_html.write(out)
print 'DONE!'
