import sys
import json
from pprint import pprint

try:
    file_name = sys.argv[1];
    with open(file_name, "r") as f:
        json_data = json.load(f)
        for course in json_data["nodes"]:
            pprint(course)
            print "\n"
            
except:
    print "Department name not valid"
