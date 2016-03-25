import json
from pprint import pprint

with open("ext/course-data-uwccs.json") as w:
    data = json.load(w)
    pprint(data)
