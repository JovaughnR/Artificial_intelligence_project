"""@author Jovaughn Rose"""

from pyswip import Prolog
from database import Database


# Initialize a database object
db = Database(
   host="localhost", 
   user="root", 
   password="", 
   db="ai_project"
)

prolog = Prolog()
prolog.consult('calculator.pl')


def calculate_total_GP(stdID: int, semester: int) -> float:
   """
      returns the sum of the `Grade Points` earned for 1 
      student for 1 semester
   """
   grade_pts = db.get_GP_byStdID(stdID, semester)
   pl_grade_pts = f"[{','.join(map(str, grade_pts))}]"

   query = f"calculate_total_grade_points({pl_grade_pts}, X)"
   result = list(prolog.query(query))

   if result:
      return result[0]['X']
   
   raise ValueError("No grade points found in Database")

def calculate_total_Credits(stdID: int, semester: int) -> float:
   """
      Returns the sum of `Credits` earned by one 
      student for one semester.
   """
   credits = db.get_credits_byStdID(stdID, semester)
   pl_credits = f"[{','.join(map(str, credits))}]"

   query = f"calculate_total_credits({pl_credits}, X)"
   result = list(prolog.query(query))

   if result:
      return result[0]['X']
   
   raise ValueError("No credits found in Database")


def calculate_GPA(stdID: int, semester: int) -> float:
   """
      returns `Grade Point Average (GPA)` earned by a
      student for 1 semester
   """
   sum_GP = calculate_total_GP(stdID, semester)
   sum_Cred = calculate_total_Credits(stdID, semester)

   query = f"calculate_semester_GPA({sum_GP}, {sum_Cred}, GPA)"
   result = list(prolog.query(query))

   if result:
      return result[0]['GPA']
   
   raise ValueError("No student data in Database")

def calculate_cumulative_GPA(stdID):
   """
      returns `Cumulative GPA` earned for 1 
      student for over multiple semesters
   """
   # check if student is registered for each semester
   semesters = db.get_registered_semesters(stdID)
   if not semesters:
      raise LookupError("Student is not registered in Database")
   
   cumulative_GPAs = []
  
   for semester in semesters:
      gpa = calculate_GPA(stdID, semester)
      cumulative_GPAs.append(gpa)

   if len(cumulative_GPAs) == 1:
      return cumulative_GPAs[0]

   sem1_GPA, sem2_GPA = cumulative_GPAs

   query = f"calculate_cumulative_GPA({sem1_GPA}, {sem2_GPA}, GPA)"
   result = list(prolog.query(query))

   if result:
      return result[0]['GPA']
   
   raise ValueError("Failed to calculate cumulative GPA for student")

def assign_grade(stdID:int, modulecode:str) -> str:
   """
      Returns a grade based on a student's score for a module
   """
   grade_point = db.get_singleGP_byStdID(stdID, modulecode)

   query = f"grade_point({grade_point}, Grade)"
   result = list(prolog.query(query))

   if result:
      return result[0]['Grade']

   raise ValueError("Failed to retrieve a Grade for student")


studID = input("Enter student ID: ")
module_code = input("Enter module code: ")


total_GP = calculate_total_GP(studID, 1)
print("Total Grade Points:", total_GP)

total_credits = calculate_total_Credits(studID, 1)
print("Total Credits:", total_credits)

gpa1 = calculate_GPA(studID, 1)
gpa2 = calculate_GPA(studID, 2)
print(f"GPA for semester 1: {gpa1}")
print(f"GPA for semester 2: {gpa2}")

cumulative_GPA = calculate_cumulative_GPA(studID)
print("Cumulative GPA:", cumulative_GPA)


grade = assign_grade(studID, module_code)
print("Grade:", grade)


