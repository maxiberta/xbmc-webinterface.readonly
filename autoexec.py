import os
import datetime
import xml.etree.cElementTree as ET

EXPORT_PATH = '/net/openwrt/mnt/sda1/shared/tmp'
HTML_PATH = '/net/openwrt/mnt/sda1/shared/movies/'

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
    %   if 'path' in movie and movie['path']:
    <div class="movie">
      <a href="${movie['path']}">
      <div>
        <img src="https://raw.github.com/tuupola/jquery_lazyload/1.9.x/img/grey.gif" data-original="${movie['thumb']}" width="130" height="190">
      </div>
      <p>${movie['title']} (${movie['year']})</p>
      </a>
      % if 'subs' in movie and movie['subs']:
      - <a href="${movie['subs']}">(subs)</a>
      % endif
    </div>
    %   endif
    % endfor
  </body>
</html>'''

tree = ET.parse(os.path.join(EXPORT_PATH, 'xbmc_videodb_%s/videodb.xml' % datetime.date.today().strftime('%Y-%m-%d')))

ATTRS = ('title', 'director', 'year', 'plot', 'basepath', 'filenameandpath', 'thumb')
movies = []
for movie in tree.findall('movie'):
    data = {}
    for attr in ATTRS:
        data[attr] =  movie.find(attr).text
    if data['basepath'].startswith(HTML_PATH):
        data['path'] = data['basepath'][len(HTML_PATH):]
    data['subs'] = None
    movies.append(data)

movies.sort(key=lambda movie: movie['title'])

from mako.template import Template
template = Template(html, output_encoding='utf-8', encoding_errors='replace')
print template.render(movies=movies)
