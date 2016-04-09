# Course Focus

Course focus is a data visualization of the relationships between
the courses at the University of Washington. It allows users
to see the prerequisites of a course and the courses that have
the given course as a prerequisite. 

Currently under development. 
###Features
 * Visualizes relationships between a course, its prerequisites
   and the courses it is a prerequisite for
 * Works for any department at UW (in development, currently 
   just the College of Arts and Sciences 

###Installation
######Dependancies
 * BeautifulSoup 4.4.0
 * lxml 3.4.4
   
###Usage
Takes uppercase department code after main.py.

Department codes can be found at:
http://www.washington.edu/about/academics/departments/
```bash
python main.py [dept-code]
```

Written in Python 2.
