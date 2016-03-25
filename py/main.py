# importing:
# regex, requests, urllib, argv, and beautiful soup

import json
from helpers import *
from pprint import pprint
import re

json_output = {}

as_codes = ["AFRAM", "AES", "AAS", "CHSTU", "SWA", "TAGLG",
            "AIS", "ANTH", "ARCHY", "BIO A", "AMATH", "CFRM",
            "ARCTIC", "ART", "ART H", "DESIGN", "ASIAN", "BENG",
            "CHIN", "HINDI", "INDN", "INDO", "JAPAN", "KOREAN",
            "SNKRT", "THAI", "URDU", "VIET", "ASTBIO", "ASTR",
            "ATM S", "BIOL", "CS SS", "CSDE", "HUM", "CHEM",
            "CL AR", "CL LI", "CLAS", "GREEK", "LATIN", "COM",
            "CHID", "C LIT", "CSE", "FRENCH", "ITAL", "GWSS",
            "GIS", "GEN ST", "INDIV", "GEOG", "GERMAN", "HSTAM",
            "HSTCMP", "HIST", "HSTAFM", "HSTAS", "HSTLAC",
            "HSTEU", "HSTAA", "HSTRY", "HPS", "INTSCI", "ISS",
            "JSIS", "JSIS A", "JSIS B", "JSIS C", "JSIS D",
            "JSIS E", "LSJ", "ASL", "LING", "MATH", "MICROM",
            "MUSIC", "MUSAP", 'MUSED', 'MUSEN', 'MUHST', 'MUSICP',
            'ARAB', 'ARAMIC', 'COPTIC', 'EGYPT', 'GEEZ', 'HEBR',
            'BIBHEB', 'MODHEB', 'NEAR E', 'PRSAN', 'CHGTAI', 'KAZAKH',
            'KYRGYZ', 'UYGUR', 'UZBEK', 'TURKIC', 'TKISH', "UGARIT",
            'NBIO', 'PHIL', 'VALUES', 'PHYS', 'POL S', 'PSYCH', 'DANISH',
            'ESTO', 'FINN', 'LATV', 'LITH', 'NORW', 'SCAND', 'SWED', 'BCS',
            "BULGR", "CZECH", "POLSH", 'ROMN', 'RUSS', 'SLAV', 'SLAVIC', 'SLVN',
            'UKR', "SOCSCI", "SOC", "PORT", "SPAN", "SPLING", "SPHSC", "STAT"]

# sorting the department codes
as_codes.sort()

for dept_code in as_codes:
    print "Accessing " + dept_code + " data..."
    dept_json = {}
    # constructing regex patterns
    # for this dept_code  
    dept_patt = re.compile(dept_code.lower()+"\d\d\d")
    # for other depts
    coursePatt = re.compile("[A-Z].[A-Z]{1,4}\s\d\d\d")

    # getting soup for this dept_code
    soup = get_soup(download_course_data(dept_code))
    remove_downloaded_data(dept_code)
    print "Finished getting " + dept_code + " data"
    print "Creating connections for " + dept_code + "..."
    # finding each course in the department
    for tag in get_tags(dept_patt, soup):
        # only concerned with first child
        content = tag.findAll()[0]
        course_name = get_course_name(content, dept_code)
        course_id = course_name.replace(" ", "").lower()

        # filtering out grad level courses
        numCID = int(float(course_id[len(dept_code):]))
        if numCID < 500:
            rawList = get_raw_prereq_list(content)
            reg_prereqs = get_reg_prereqs(rawList, coursePatt)
            choice_prereqs = get_choice_prereqs(rawList, coursePatt)
            course_info = get_course_info(content)
             
            # creating JSON object to represent current node
            course_json = {u"course_id": course_id, u"reg_prereqs": reg_prereqs,
                           u"choice_prereqs": choice_prereqs, u"numCID": numCID,
                           u"course_info": course_info, u"course_name": course_name}
            dept_json[course_id] = course_json
    print "Adding " + dept_code + " to JSON...\n"
    json_output[dept_code] = dept_json


with open("ext/course-data-uwccs.json", "w") as outfile:
    json.dump(json_output, fp=outfile)

pprint(json_output["FRENCH"])
