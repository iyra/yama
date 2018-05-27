yama - a static site generator

Yama takes content of various types (like page or essay) and
treats them as categories; you can edit the members of these
categories under the "content" directory. You can then create
lists of these items (see templates/index.html for examples),
which saves a lot of the work of keeping track of dates and
lists of your content.

The output is put in output/ and is pure HTML. There is currently
no support for assets, but it is planned, along with modifications
to let you make a gallery out of pictures in a directory. See
sync.sh for an example use case to generate pages and 
upload them to your web server.

The Jinja2 template system is used. It has only been tested on
GNU/Linux with Python 3.7. BeautifulSoup 4, dateutil and Jinja2
are requirements.

This work is made available under the CC0 1.0 Universal Public
Domain dedication, available here: 
https://creativecommons.org/publicdomain/zero/1.0/
