import LinkGenerator
import json

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


for dept_code in asCodes:
    dept_node_dict = LinkGenerator.get_dept_node_dict("ext/course-data-uwccs.json", dept_code)
    node_list = LinkGenerator.generate_node_list(dept_node_dict)
    link_list = LinkGenerator.generate_links(node_list)

    # setting up JSON output file
    json_output = {"nodes": node_list,
                   "links": link_list}

    with open("ext/" + dept_code + "-force.json", "w") as outfile:
        json.dump(json_output, fp=outfile)
