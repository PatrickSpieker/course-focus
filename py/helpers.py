import urllib
from bs4 import BeautifulSoup
import os


def download_course_data(dept_code):
    # base url
    url = "http://www.washington.edu/students/crscat/" + dept_code.lower() + ".html"
    destination = dept_code + "CourseData.html"
    # fetching HTML
    urllib.urlretrieve(url, destination)
    return destination


def remove_downloaded_data(dept_code):
    os.remove(dept_code + "CourseData.html")


def get_soup(target):
    # opening file
    with open(target, "r") as f:
        data = f.read()
    # processing data
    soup = BeautifulSoup(data, "lxml")
    return soup


# takes regex pattern and Soup object
# returns list of relevant tags
def get_tags(pattern, soup):
    tags = soup.find_all("a", attrs={"name": pattern})
    return tags


# TODO: finish out actual return conditional
def get_courses_off_with(contents):
    # checking to see if there are any relevant courses
    info_idx = str(contents).find("Prerequisite: ")
    if info_idx == -1:
        return []
    info_idx += len("Prerequisite: ")


def has_prereqs(content):
    return not (str(content).find("Prerequisite: ") == -1)


def has_off_w(content):
    return not (str(content).find("Offered") == -1)


def get_relevant_end_idx(str_content, relevant_start_idx):
    if str_content.find("Offered: jointly") != -1:
        return str_content.find("Offered: jointly")
    return str_content.find("<br/>", relevant_start_idx)


def get_raw_prereq_list(content):
    if not has_prereqs(content):
        return []
    str_content = str(content)
    relevant_start_idx = str_content.find("Prerequisite: ")+len("Prerequisite: ")
    relevant_end_idx = get_relevant_end_idx(str_content, relevant_start_idx)
    relevant_content = str(content)[relevant_start_idx:relevant_end_idx]
    # splitting into each seperate prereq
    return relevant_content.split(";")


def get_course_info(content):
    str_content = str(content)
    if has_prereqs(content):
        desc_end_idx = str_content.find("Prerequisite: ")
    elif has_off_w(content):
        desc_end_idx = str_content.find("Offered: jointly")
    else:
        desc_end_idx = len(str_content)-1
    desc = str_content[0:desc_end_idx]
    return desc


def get_reg_prereqs(raw_prereq_list, course_patt):
    if not raw_prereq_list:
        return []
    reg_prereqs = []
    for section in raw_prereq_list:
        # checking for optional prereqs
        if "or" not in section:
            # append EACH ITEM from the list of options
            for item in course_patt.findall(section):
                reg_prereqs.append(item.replace(" ", "").lower())
    return reg_prereqs


def get_choice_prereqs(raw_prereq_list, course_patt):
    if not raw_prereq_list:
        return []
    choice_prereqs = []
    for section in raw_prereq_list:
        # checking for optional prereqs
        if "or" in section:
            # append the ENTIRE tuple of options to the prereq list
            options = course_patt.findall(section)
            section_choices = [option.replace(" ", "").lower() for option in options]
            choice_prereqs.append(section_choices)
    return choice_prereqs


def get_course_name(content, dept_code):
    # defining string with course info
    course_str = content.b.string
    # finding length of course_name
    name_end = len(dept_code.lower())+4  # length of space and number
    # defining course name, ex: CSE 143
    course_name = course_str[0:name_end]
    return course_name
