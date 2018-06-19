#!/usr/bin/env python

DATA_PATH="devworld.json"
CSS_PATH="css/devworld.css"

import json
import jinja2

import hashlib

from jinja2 import Template

from bs4 import BeautifulSoup

import markdown

def main():
    
    templateLoader = jinja2.FileSystemLoader( searchpath="templates" )
    templateEnv = jinja2.Environment( loader=templateLoader )

    md = markdown.Markdown(extensions=['meta'])

    templateEnv.filters['markdown'] = lambda text: jinja2.Markup(md.convert(text))
    templateEnv.globals['get_title'] = lambda: md.Meta['title'][0]
    templateEnv.trim_blocks = True
    templateEnv.lstrip_blocks = True

    data = json.load(open(DATA_PATH))

    sha1 = hashlib.sha1()

    with open(CSS_PATH, 'rb') as f:
        buf = f.read()
        sha1.update(buf)
    
    data["css_version"] = sha1.hexdigest()[:7]

    template = templateEnv.get_template( "index.html" )

    document = template.render (data)

    print(document)

    #soup = BeautifulSoup(document, 'html.parser')


    #document, errors = tidy_document(document)

    #print (soup.prettify())

    #if len(errors) > 0:
    #    print ("<!-- " + errors + " -- >")

    # template = open("templates/talks.html").read()

    # sessions_1 = 

if __name__ == '__main__':
    main()

