#!/usr/bin/env python

import json
import jinja2
import hashlib
import markdown
import os
from os import path as op

import sqlite3

from jinja2 import Template

import dateutil

from collections import defaultdict

from  dateutil.parser import parse as parsedate

from pprint import pprint

DATA_PATH="devworld.json"
CSS_PATH="css/devworld.css"

INDEX_PATH="index.html"
TALKS_DIR_PATH="sessions"
SCHEDULE_PATH="schedule.html"

def main():

    # set up our jinja loader and environment
    
    templateLoader = jinja2.FileSystemLoader( searchpath="templates" )
    templateEnv = jinja2.Environment( loader=templateLoader )

    # add a filter for rendering markdown

    md = markdown.Markdown(extensions=['meta'])

    templateEnv.filters['markdown'] = lambda text: jinja2.Markup(md.convert(text))
    templateEnv.trim_blocks = True
    templateEnv.lstrip_blocks = True

    def _jinja2_filter_datetime(date, fmt=None):
        date = dateutil.parser.parse(date)
        native = date.replace(tzinfo=None)
        format= fmt or '%b %d, %Y'
        return native.strftime(format) 
    
    templateEnv.filters['parsedate'] = _jinja2_filter_datetime

    # load the data we got

    data = fetch_data()

    pprint(data)

    # We want to ensure that browsers don't cache old versions of the CSS,
    # so we hash it every time we generate the index and include that at
    # the end of the URL (eg devworld.css?v=abcde12), so that each revision
    # of the css has a unique URL
    sha1 = hashlib.sha1()

    with open(CSS_PATH, 'rb') as f:
        buf = f.read() # 
        sha1.update(buf)
    
    data["css_version"] = sha1.hexdigest()[:7]

    #schedule_data = generate_schedule(data["talks"])

    #data["schedule"] = schedule_data

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
        talk_document = talk_template.render({"css_version": data["css_version"], **talk})
        with open(path, "w") as f:
            f.write(talk_document)
            print("Wrote {} for talk {}".format(path, talk["title"]))
    
    schedule_template = templateEnv.get_template("schedule.html")

    schedule_document = schedule_template.render(data)

    with open(SCHEDULE_PATH, "w") as f:
         f.write(schedule_document)

    # print("Wrote schedule to {}".format(SCHEDULE_PATH))

def fetch_data():
    conn = sqlite3.connect('data/devworld.db')

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn.row_factory = dict_factory

    c = conn.cursor()



    data = {}

    data["talks"] = c.execute("SELECT * FROM talks;").fetchall()

    for talk in data["talks"]:        
        speakers = c.execute("Select speakers.* from speakers_talks st inner join speakers on speakers.id = st.speaker_id where st.talk_id = \"{0}\"".format(talk["id"])).fetchall();

        talk["speakers"] = speakers
    
    data["images"] = c.execute("SELECT * FROM images ORDER BY image;").fetchall()

    data["team"] = c.execute("SELECT * FROM speakers WHERE is_team = 1").fetchall()

    conn.close()

    return data

def generate_schedule(events):

    def group_events_by_day(events):
        d = defaultdict(list)
        for event in events:
            date = parsedate(event["date"])
            d[date.isoformat()].append(event)
        
        return d
    
    def group_day_by_time(events):
        d = defaultdict(list)
        for event in events:
            date = parsedate(event["date"] + " " + event["start"])
            d[date.isoformat()].append(event)
        return d
    
    final_groups = {day: group_day_by_time(day_events) for day, day_events in group_events_by_day(events).items()}

    return final_groups

def update_events():
    import dateutil.tz
    data = json.load(open("devworld.json"))

    def update_event(event):
        start = parsedate(event["date"] + " " + event["start"])
        end = parsedate(event["date"] + " " + event["end"])

        timezone = dateutil.tz.gettz("Australia/Melbourne")

        start = start.replace(tzinfo=timezone)
        end = end.replace(tzinfo=timezone)

        return {**event, **{"start_iso": start.isoformat(), "end_iso": end.isoformat()}}
    
    data["talks"] = [update_event(e) for e in data["talks"]]

    json.dump(data, open("devworld.json", "w"), indent=4)



if __name__ == '__main__':
    main()

