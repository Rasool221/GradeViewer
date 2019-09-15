import requests
import datetime

API_KEY = "Bearer api-key-goes-here"
CANVAS_DOMAIN = "https://domain.goes/here"
COURSES_ENDPOINT = "/api/v1/courses?include[]=total_scores"
STUDENTS_ENDPOINT = "/api/v1/courses/{}/users?include[]=email&per_page=100"
ASSIGNMENTS_ENDPOINT = "/api/v1/users/self/courses/{}/assignments"

auth = {"Authorization":API_KEY}

def get_courses():
    response = requests.get(CANVAS_DOMAIN + COURSES_ENDPOINT, headers=auth)
    
    classes_dict = response.json()

    for classes in classes_dict:
        print("\n", "(id:{})".format(classes["id"]), classes["name"], end="")
        
        for items in classes["enrollments"]:
            try:
                if (str(items["computed_current_grade"]) != "None"):
                    print("\tGrade ->", items["computed_current_grade"], "({}%)".format(items["computed_current_score"]))
                else:
                    print("\tGrade ->", items["computed_current_grade"])
            except:
                pass


def get_students(course_id):
    response = requests.get(CANVAS_DOMAIN + STUDENTS_ENDPOINT.format(course_id), headers=auth)
    students_dict = response.json()

    for students in students_dict:
        print("(id:{})".format(students["id"]), students["name"])

def get_assignments(course_id):
    response = requests.get(CANVAS_DOMAIN + ASSIGNMENTS_ENDPOINT.format(course_id), headers=auth)
    assignment_dict = response.json()

    for assignments in assignment_dict:
        print("\n", assignments["name"])
       
while (True):
    cmd = input()
    before = datetime.datetime.now()

    if (cmd == "courses"):
        get_courses()
    elif (cmd == "quit" or cmd == "exit()" or cmd == "q"):
        exit()
    elif ("students in" in cmd):
        get_students(cmd.replace("students in ", ""))
    elif ("assignments in" in cmd):
        get_assignments(cmd.replace("assignments in ", ""))
    elif (cmd == "help"):
        print("\nAvaliable commands:\n")
        print("courses", "(Views the current courses you are enrolled in)\n")
        print("students in <course_id>", "(Prints a list of students in that course)\n")
        print("assignments in <course_id>", "(Prints a list of assignments in that course)\n")
        print("quit, exit(), or q", "(Exits the program)\n")
    
    print("\nExecution time:", str(datetime.datetime.now()-before), "\n")


