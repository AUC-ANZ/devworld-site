#!/usr/bin/env python

import sqlite3


import os



from pprint import pprint


locations = {}

# class Session(Object):
#     def __repr__(self):
#         return f"Session: {self.title}; speakers={self.speakers}" 
    
#     def __iter__(self):
#         # first start by grabbing the Class items
#         iters = dict((x,y) for x,y in Session.__dict__.items() if x[:2] != '__')

#         # then update the class items with the instance items
#         iters.update(self.__dict__)

#         # now 'yield' through the items
#         for x,y in iters.items():
#             yield x,y

# class Location(Object):
#     pass

# class Speaker(Object):
#     def __iter__(self):
#         # first start by grabbing the Class items
#         iters = dict((x,y) for x,y in Session.__dict__.items() if x[:2] != '__')

#         # then update the class items with the instance items
#         iters.update(self.__dict__)

#         # now 'yield' through the items
#         for x,y in iters.items():
#             yield x,y

def fetch_data_parse():

    from dotenv import load_dotenv

    load_dotenv()

    os.environ["PARSE_API_ROOT"] = os.getenv("SERVER_URL")

    from parse_rest.datatypes import Function, Object, GeoPoint, Pointer, File
    from parse_rest.connection import register
    from parse_rest.query import QueryResourceDoesNotExist
    from parse_rest.connection import ParseBatcher
    from parse_rest.core import ResourceRequestBadRequest, ParseError

    from parse_rest.datatypes import Object


    register(os.getenv("APP_ID"), "", master_key=os.getenv("MASTER_KEY"))



    all_talks = Session.Query.all()

    data = {}

    for session in all_talks:
        #print(dict(session))
        print (session.title)

        s = dict(session)
        s["speakers"] = []

        speakers = session.speakers.query()

        for sp in speakers:
            #s["speakers"].append(dict(sp))
            print(sp.name)


        

        
        

    
    #pprint(all_talks)


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

    data["talks"] = c.execute("SELECT * FROM talks WHERE talks.status == 'Confirmed' or talks.status == 'ConfirmedHidden';").fetchall()

    for talk in data["talks"]:        
        speakers = c.execute("Select speakers.* from speakers_talks st inner join speakers on speakers.id = st.speaker_id where st.talk_id = \"{0}\"".format(talk["id"])).fetchall()

        talk["speakers"] = speakers
    
    data["images"] = c.execute("SELECT * FROM images ORDER BY image;").fetchall()

    data["team"] = c.execute("SELECT * FROM speakers WHERE is_team = 1").fetchall()

    data["speakers"] = c.execute("SELECT * FROM accepted_speakers;").fetchall()

    conn.close()

    return data

if __name__ == "__main__":
    fetch_data_parse()