#!/usr/bin/env python

import json
import jinja2
import hashlib
import markdown
import os
from os import path as op

from jinja2 import Template

DATA_PATH="devworld.json"
CSS_PATH="css/devworld.css"

INDEX_PATH="index.html"
TALKS_DIR_PATH="sessions"

def main():

    # set up our jinja loader and environment
    
    templateLoader = jinja2.FileSystemLoader( searchpath="templates" )
    templateEnv = jinja2.Environment( loader=templateLoader )

    # add a filter for rendering markdown

    md = markdown.Markdown(extensions=['meta'])

    templateEnv.filters['markdown'] = lambda text: jinja2.Markup(md.convert(text))
    templateEnv.trim_blocks = True
    templateEnv.lstrip_blocks = True

    # load the data we got

    data = json.load(open(DATA_PATH))

    # We want to ensure that browsers don't cache old versions of the CSS,
    # so we hash it every time we generate the index and include that at
    # the end of the URL (eg devworld.css?v=abcde12), so that each revision
    # of the css has a unique URL
    sha1 = hashlib.sha1()

    with open(CSS_PATH, 'rb') as f:
        buf = f.read() # 
        sha1.update(buf)
    
    data["css_version"] = sha1.hexdigest()[:7]

    # render the template
    index_template = templateEnv.get_template( "index.html" )
    
    document = index_template.render (data)
    
    with open(INDEX_PATH, "w") as f:
        f.write(document)
        print("Wrote {}".format(INDEX_PATH))
    
    talks = data["talks"]

    talk_template = templateEnv.get_template("talk.html")

    os.makedirs(TALKS_DIR_PATH, exist_ok=True)

    for talk in talks:
        if talk["type"] == "admin":
            continue
        path = op.join(TALKS_DIR_PATH, "{0}.html".format(talk["id"]))
        talk_document = talk_template.render(talk)
        with open(path, "w") as f:
            f.write(talk_document)
            print("Wrote {} for talk {}".format(path, talk["title"]))
        


if __name__ == '__main__':
    main()

