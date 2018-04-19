#!/usr/bin/env python

import json

DATA="gallery.json"

data = json.load(open(DATA))

for i, image in enumerate(data):

    if i >= 4:
        display_class = "d-sm-none"
    else:
        display_class = ""

    print('<div class="col col-md-3 col-sm-12 {}">'.format(display_class))
    if "url" in image:
        print('    <a href="{}">'.format(image["url"]))
    print('    <img src="images/gallery/final/{}" />'.format(image["img"]))

    if "url" in image:
        print('    </a>')
    print('</div>')
    