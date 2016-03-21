# importing:
# regex, requests, urllib, argv, and beautiful soup

import json
from helpers import *
from pprint import pprint
import re

json_output = {}

asCodes = ["AFRAM", "AES", "AAS", "CHSTU", "SWA", "TAGLG",
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
asCodes.sort()

for deptCode in asCodes:
    print "Accessing " + deptCode + " data..."
    deptJSON = {}
    # constructing regex patterns
    # for this deptCode  
    deptPatt = re.compile(deptCode.lower()+"\d\d\d")
    # for other depts
    coursePatt = re.compile("[A-Z].[A-Z]{1,3}\s\d\d\d")

    # getting soup for this deptCode
    soup = getSoup(downloadCourseData(deptCode))
    removeDownloadedData(deptCode)
    print "Finished getting " + deptCode + " data"
    print "Creating connections for " + deptCode + "..."
    # finding each course in the department
    for tag in getTags(deptPatt, soup):
        # only concerned with first child
        content = tag.findAll()[0]
        courseId = getCourseId(content, deptCode)
        courseClass = courseId.replace(" ", "").lower()

        # filtering out grad level courses
        numCID = int(float(courseId[len(deptCode):]))
        if numCID < 500:
            rawList = getRawPrereqList(content)
            regPrereqs = getRegPrereqs(rawList, coursePatt)
            choicePrereqs = getChoicePrereqs(rawList, coursePatt)
             
            # creating JSON object to represent current node
            courseInfo = {u"course_id": courseId, u"regPrereqs": regPrereqs,
                    u"choicePrereqs": choicePrereqs, u"numCID": numCID}
            deptJSON[courseClass] = courseInfo
    print "Adding " + deptCode + " to JSON...\n"
    json_output[deptCode] = deptJSON


with open("ext/course-data-uwccs.json", "w") as outfile:
    json.dump(json_output, fp=outfile)






