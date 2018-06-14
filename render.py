#!/usr/bin/env python

DATA_PATH="devworld.json"



import json
import jinja2

from jinja2 import Template


def main():
    
    templateLoader = jinja2.FileSystemLoader( searchpath="templates" )
    templateEnv = jinja2.Environment( loader=templateLoader )

    data = json.load(open(DATA_PATH))



    
    template = templateEnv.get_template( "talks.html" )
    print (template.render( data ))

    # template = open("templates/talks.html").read()

    # sessions_1 = 

if __name__ == '__main__':
    main()

