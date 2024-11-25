"""@author Jovaughn Rose"""
from pyswip import Prolog
from database import Database

KnowledgeBase = 'calculator.pl'

class PrologCalculator:
   def __init__(self, database:Database):
      """Initialize the Prolog calculator with a database and Prolog knowledgebase file."""
      self.db = database
      self.prolog = Prolog()
      self.consult = self.prolog.consult

   def load(self):
      self.knowledgebase = KnowledgeBase

   def calculate_sum_GP_credits(self, stdID: int, semester: int, year: str) -> float:
      """Returns the sum of the `Grade Points * module credits` for a student in a semester."""
      grade_pts, credits = self.db.get_GP_Credit(stdID, semester, year)
      pl_grade_pts = f"[{','.join(map(str, grade_pts))}]"
      pl_credits = f"[{','.join(map(str, credits))}]"

      self.consult(KnowledgeBase)
      query = f"calculate_sum_GP_semester({pl_credits}, {pl_grade_pts}, X)"
      result = list(self.prolog.query(query))

      if result:
         return result[0]['X']   
      return False

   def calculate_total_credits(self, stdID: int, semester: int, year) -> float:
      """Returns the sum of `Credits` for a student in a semester."""
      credits = self.db.get_credits_byID(stdID, semester, year)
      pl_credits = f"[{','.join(map(str, credits))}]"

      self.consult(KnowledgeBase)
      query = f"calculate_total_credits({pl_credits}, X)"
      result = list(self.prolog.query(query))

      if result:
         return result[0]['X']
      return False

   def calculate_GPA(self, stdID: int, semester: int, year: str) -> float:
      """Calculates and returns the `GPA` for a student in a semester."""
      sum_GP = self.calculate_sum_GP_credits(stdID, semester, year)
      sum_Cred = self.calculate_total_credits(stdID, semester, year)

      self.consult(KnowledgeBase)
      query = f"calculate_semester_GPA({sum_GP}, {sum_Cred}, GPA)"
      result = list(self.prolog.query(query))

      if result:
         return f"{result[0]['GPA']:.2f}"
      
      return False

   def cumulative_GPA(self, stdID: int, year:str) -> float:
      """Calculates and returns the `Cumulative GPA` for a student across multiple semesters."""
      semesters = self.db.get_registered_semesters(stdID, year)
      if not semesters:
         raise LookupError("Student is not registered in Database")
      
      if len(semesters) == 1:
         return self.calculate_GPA(stdID, semesters[0], year)

      # Get all credits and grade points across semesters
      all_GP = []
      all_cred = []

      for semester in semesters:
         sem_GP, sem_cred = self.db.get_GP_Credit(stdID, semester, year)
         all_GP.extend(sem_GP)
         all_cred.extend(sem_cred)

      # Convert lists to Prolog-compatible format
      pl_all_GP = f"[{','.join(map(str, all_GP))}]"
      pl_all_cred = f"[{','.join(map(str, all_cred))}]"

      # Calculate total grade points and credits
      query = f"calculate_sum_GP_semester({pl_all_GP}, {pl_all_cred}, X)"
      total_GP = list(self.prolog.query(query))[0]['X']

      self.consult(KnowledgeBase)
      query = f"calculate_total_credits({pl_all_cred}, X)"
      total_credits = list(self.prolog.query(query))[0]['X']

      # Calculate cumulative GPA
      query = f"calculate_cumulative_GPA({total_GP}, {total_credits}, GPA)"
      result = list(self.prolog.query(query))

      if result:
         return f"{result[0]['GPA']:.2f}"
      
      return False

   def assign_grade(self, stdID: int, module_code: str) -> str:
      """Assigns and returns a grade based on a student's score for a module."""
      grade_point = self.db.get_singleGP_byStdID(stdID, module_code)

      self.consult(KnowledgeBase)
      query = f"grade_point({grade_point}, Grade)"
      result = list(self.prolog.query(query))

      if result:
         return result[0]['Grade']
      raise ValueError("Failed to retrieve a Grade for student")
   
   def get_grade(self, grade_point):
      query = f"grade_point({grade_point}, Grade)"
      try:
         self.consult(KnowledgeBase)
         result = list(self.prolog.query(query))
         return result[0]['Grade']
      except Exception as e:
         return False
      
   def update_gpa_threshold(self, new_gpa):
      try:
         with open(KnowledgeBase, 'r') as kb:
            lines = kb.readlines()

         with open(KnowledgeBase, 'w') as kb:
            for line in lines:
               if line.strip().startswith("default_gpa("):
                  kb.write(f"default_gpa({new_gpa}).\n")
               else:
                  kb.write(line)
            return True
      except Exception as e:
         return False
      
   def get_default_gpa(self):
      self.consult(KnowledgeBase)
      query = "default_gpa(X)"
      result = list(self.prolog.query(query)) 
      if result:  
         return result[0]['X']  
      return None  



# prolog = Prolog()
# # prolog.consult('calculator.pl')

# db = Database(
#    host="localhost", 
#    user="root", 
#    password="", 
#    db="ai_project"
# )

# pl = PrologCalculator(db, 'calculator.pl')
# grade = pl.get_grade(2.4)
# print("Grade:", grade)
# print(pl.get_default_gpa())


# studID = input("Enter student ID: ")
# module_code = input("Enter module code: ")
# # print(pl.calculate_cumulative_GPA(2111876))


# total_GP = pl.calculate_total_GP(studID, 1)
# print("Total Grade Points:", total_GP)

# total_credits = pl.calculate_total_credits(studID, 1)
# print("Total Credits:", total_credits)

# gpa1 = pl.calculate_GPA(studID, 1)
# gpa2 = pl.calculate_GPA(studID, 2)


# print(f"GPA for semester 1: {gpa1}")
# print(f"GPA for semester 2: {gpa2}")

# cumulative_GPA = pl.calculate_cumulative_GPA(studID)
# print("Cumulative GPA:", cumulative_GPA)


# grade = pl.assign_grade(studID, module_code)
# print("Grade:", grade)

# # while True:
# #    sentence = input("Enter query: ")
# #    if "end" == sentence.lower():
# #       break
# #    print(predict(sentence))


