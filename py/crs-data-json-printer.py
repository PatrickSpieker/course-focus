import sys
import json
from pprint import pprint

try:
    file_name = sys.argv[1];
    with open(file_name, "r") as f:
        json_data = json.load(f)
        if len(sys.argv) == 3:
            dept_name = sys.argv[2];  
            pprint(json_data[dept_name])
        else:
            for dept in json_data:
                pprint(dept)
                pprint(json_data[dept])
                print "\n"
            
except Exception as e:
    print e

