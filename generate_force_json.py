import LinkGenerator
import sys
import json

try:
    dept = str(sys.argv[1])
except IndexError:
    print("You must pass the department code as an argument!")
    sys.exit(0)

dept_node_dict = LinkGenerator.get_dept_node_dict("ext/course-data-uwccs.json", dept)
node_list = LinkGenerator.generate_node_list(dept_node_dict)
link_list = LinkGenerator.generate_links(node_list)

# setting up JSON output file
json_output = {"nodes": node_list,
               "links": link_list}

with open("ext/force-data.json", "w") as outfile:
    json.dump(json_output, fp=outfile)



