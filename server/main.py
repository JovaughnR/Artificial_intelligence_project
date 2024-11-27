"""@author Jovaughn Rose"""

from pyswip import Prolog
from database import Database

class PrologCalculator:
    def __init__(self, database: Database, knowledge_base: str = 'calculator.pl'):
        """
        Initialize the Prolog calculator with a database and Prolog knowledge base file.
        """
        self.db = database
        self.prolog = Prolog()
        self.knowledge_base = knowledge_base
        self._consult_knowledge_base()

    def _consult_knowledge_base(self):
        """
        Consult the Prolog knowledge base.
        """
        try:
            self.prolog.consult(self.knowledge_base)
        except Exception as e:
            raise RuntimeError(f"Failed to load Prolog knowledge base: {e}")

    def _query_prolog(self, query: str):
        """
        Execute a query in Prolog and return the result.
        """
        try:
            result = list(self.prolog.query(query))
            return result
        except Exception as e:
            print(f"Error executing Prolog query '{query}': {e}")
            return None

    def calculate_sum_GP_credits(self, stdID: int, semester: int, year: str) -> float:
        """
        Returns the sum of `Grade Points * module credits` for a student in a semester.
        """
        grade_pts, credits = self.db.get_GP_Credit(stdID, semester, year)
        pl_grade_pts = f"[{','.join(map(str, grade_pts))}]"
        pl_credits = f"[{','.join(map(str, credits))}]"
        query = f"calculate_sum_GP_semester({pl_credits}, {pl_grade_pts}, X)"
        result = self._query_prolog(query)

        return result[0]['X'] if result else 0.0

    def calculate_total_credits(self, stdID: int, semester: int, year: str) -> float:
        """
        Returns the sum of credits for a student in a semester.
        """
        credits = self.db.get_credits_by_id(stdID, semester, year)
        pl_credits = f"[{','.join(map(str, credits))}]"
        query = f"calculate_total_credits({pl_credits}, X)"
        result = self._query_prolog(query)

        return result[0]['X'] if result else 0.0

    def calculate_GPA(self, stdID: int, semester: int, year: str) -> float:
        """
        Calculates and returns the GPA for a student in a semester.
        """
        sum_GP = self.calculate_sum_GP_credits(stdID, semester, year)
        total_credits = self.calculate_total_credits(stdID, semester, year)

        if not (sum_GP or total_credits):
            return 0.0
        query = f"calculate_semester_GPA({sum_GP}, {total_credits}, GPA)"
        result = self._query_prolog(query)

        return round(result[0]['GPA'], 2) if result else 0.0

    def cumulative_GPA(self, stdID: int, year: str) -> float:
        """
        Calculates and returns the cumulative GPA for a student across multiple semesters.
        """
        semesters = self.db.get_registered_semesters(stdID, year)
        if not semesters:
            return 0.0

        all_GP, all_credits = [], []
        for semester in semesters:
            sem_GP, sem_credits = self.db.get_GP_Credit(stdID, semester, year)
            all_GP.extend(sem_GP)
            all_credits.extend(sem_credits)

        pl_all_GP = f"[{','.join(map(str, all_GP))}]"
        pl_all_credits = f"[{','.join(map(str, all_credits))}]"
        query_GP = f"calculate_sum_GP_semester({pl_all_GP}, {pl_all_credits}, X)"
        total_GP = self._query_prolog(query_GP)[0]['X']

        query_credits = f"calculate_total_credits({pl_all_credits}, X)"
        total_credits = self._query_prolog(query_credits)[0]['X']

        query_GPA = f"calculate_cumulative_GPA({total_GP}, {total_credits}, GPA)"
        result = self._query_prolog(query_GPA)

        return round(result[0]['GPA'], 2) if result else 0.0

    def assign_grade(self, stdID: int, module_code: str) -> str:
        """
        Assigns and returns a grade based on a student's score for a module.
        """
        grade_point = self.db.get_single_grade_point(stdID, module_code)
        query = f"grade_point({grade_point}, Grade)"
        result = self._query_prolog(query)

        if result:
            return result[0]['Grade']
        raise ValueError("Failed to assign grade for the student.")

    def get_grade(self, grade_point: float) -> str:
        """
        Retrieves the grade associated with a given grade point.
        """
        query = f"grade_point({grade_point}, Grade)"
        result = self._query_prolog(query)

        return result[0]['Grade'] if result else "Unknown"

    def update_gpa_threshold(self, new_gpa: float) -> bool:
        """
        Updates the default GPA threshold in the knowledge base.
        """
        try:
            with open(self.knowledge_base, 'r') as kb:
                lines = kb.readlines()

            with open(self.knowledge_base, 'w') as kb:
                for line in lines:
                    if line.strip().startswith("default_gpa("):
                        kb.write(f"default_gpa({new_gpa}).\n")
                    else:
                        kb.write(line)
            self._consult_knowledge_base()
            return True
        except Exception as e:
            print(f"Error updating GPA threshold: {e}")
            return False

    def get_default_gpa(self) -> float:
        """
        Retrieves the default GPA threshold from the knowledge base.
        """
        query = "default_gpa(X)"
        result = self._query_prolog(query)

        return result[0]['X'] if result else 0.0

# db = Database(
#    host="localhost", 
#    user="root", 
#    password="", 
#    database="ai_project"
# )
# pl = PrologCalculator(db)

# while True:
#    new_gpa = float(input("update default GPA: "))
#    if new_gpa == 0.0:
#        break
#    current_gpa = pl.get_default_gpa()
#    pl.update_gpa_threshold(new_gpa)
#    print("Current GPA:", current_gpa)

# grade = pl.get_grade(2.4)
# print("Grade:", grade)
# while True:
#    user_id = int(input("Enter student ID: "))
#    print(pl.calculate_GPA(user_id, 1, '2023'))
# print(pl.get_default_gpa())


# studID = input("Enter student ID: ")
# module_code = input("Enter module code: ")
# print(pl.cumulative_GPA(2111876, 2022))


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


# grade = pl.assign_grade(21111876,)
# print("Grade:", grade)

# # while True:
# #    sentence = input("Enter query: ")
# #    if "end" == sentence.lower():
# #       break
# #    print(predict(sentence))


