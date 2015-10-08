# importing:
# regex, requests, urllib, argv, and beautiful soup
import re
import requests
import urllib
from sys import argv
from bs4 import BeautifulSoup
import simplejson as json

# picking up command line argument
dept = str(argv[1])

# empty list for all Course JSON
nodes = []
# empty list for course links
links = []

# Prereq dictionary for link creation
link_dict = {}

# base url
url = "http://www.washington.edu/students/crscat/" + dept.lower() + ".html"
# fetching HTML
urllib.urlretrieve(url, "test.html")
data = open("test.html","r").read()
soup = BeautifulSoup(data, "lxml")
# constructing regex pattern
patt = dept.lower()+"\d\d\d"


# opening file
with open("test.html", "r") as f:
    data = f.read()
# processing data
soup = BeautifulSoup(data, "lxml")
for tag in soup.find_all("a", attrs={"name":re.compile(patt)}):
    for child in tag.children:

        # identifying where prereqs will be in text
        prereq_start = str(child).find("Prerequisite: ")
        len_prereq = len("Prerequisite: ")

        # empty prereq list
        prereqs = []
        # checking to see if prereqs exist
        if prereq_start == -1:
            # no they don't
            prereqs = None
            # off_w is offered with
            off_w = None
        else:
            # yes they do
            final_part = str(child)[prereq_start+len_prereq:]
            prereq_end = final_part.find("<br/>")
            final_part = final_part[:prereq_end]

            final_part_list = final_part.split("Offered")
            # all of these now must have prereq's
            prereq_raw = final_part_list[0]
            if len(final_part_list) == 2:
                # only some will have joint classes
                off_w_raw = final_part_list[1]
                off_re = re.compile("[A-Z].[A-Z]{1,3}\s\d\d\d")
                off_w = off_re.findall(off_w_raw)
            else:
                # if they don't, connect this with correct variable
                off_w = None

            # splitting into each seperate prereq
            prereq_split = prereq_raw.split(";")
            # iterating through and regexing out excess
            for i in prereq_split:
                if "or" in i:
                    p = re.compile("[A-Z].[A-Z]{1,3}\s\d\d\d")
                    # append the ENTIRE tuple of options to the prereq list
                    if p.findall(i):
                        p_tup = tuple(p.findall(i))
                        prereqs.append(p_tup)
                        # the prereq list is tuple-ified at the end of the process
                else:
                    p = re.compile("[A-Z].[A-Z]{1,3}\s\d\d\d")
                    # append EACH ITEM from the list of options
                    for j in p.findall(i):
                        prereqs.append(j)

            # making prereqs immutable via tuple
            if prereqs:
                prereqs = tuple(prereqs)
            else:
                prereqs = tuple()

        if child.b:
            # defining string with course info
            course_str = child.b.string
            # finding index of end of course string
            course_str_end = course_str.find("(")-1
            # finding length of course_id
            id_end = len(dept.lower())+4  # length of space and number
            # defining course id, ex: CSE 143
            course_id = course_str[0:id_end]
            # defining actual name of the course
            name = course_str[8:course_str.find("(")-1]

        # creating JSON object to represent current node
        node = {u"course_id": course_id, u"name": name,
               u"prereqs": prereqs, u"off_w": off_w}
        nodes.append(node)

        # adding link to link dict
        link_dict[node[u"course_id"]] = nodes.index(node)

        # adding prereqs to node list
        #for prereq in prereqs:
         #   if type(prereq) is tuple:
          #      for act_prereq in prereq:
           #         if not link_dict[node[act_prereq]]:
                #        nodes.append({})


# for key in link_dict:
#    print key + ": " + str(link_dict[key])
for node in nodes:
    if node["prereqs"]:
        for prereq in node["prereqs"]:
            if type(prereq) is tuple:
                for act_prereq in prereq:
                    try:
                        links.append({"source": link_dict[act_prereq],
                                      "target": link_dict[node["course_id"]]
                                      })
                    except KeyError as e:
                        pass #print e
            else:
                try:
                    links.append({"source": link_dict[prereq],
                                  "target": link_dict[node["course_id"]],
                                  })
                except KeyError as e:
                    pass #print e

#



# setting up JSON output file
json_output = {"nodes": nodes,
               "links": links}

with open("course-data.json", "w") as outfile:
    json.dump(json_output, fp=outfile)


