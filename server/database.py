"""@authors: Shamar Bennett and Jovaughn Rose"""

import mysql.connector
import hashlib 

class Database:
   def __init__(self, host, user, password, db):
      self.host = host
      self.user = user
      self.password = password
      self.database = db
      self.__connect()

   # private method
   def __connect(self):
      """Initialize the connection the database"""
      self.connector = mysql.connector.connect(
         host=self.host,
         user=self.user,
         password=self.password,
         database=self.database
      )
      if self.connector.is_connected():
         print("Database connection established.")
      else:
         raise ConnectionError("Database connection failed")
      self.cursor = self.connector.cursor()

   @classmethod
   def __hash(cls, string):
      encoded_string = string.encode()
      hashObj = hashlib.sha256(encoded_string)
      hashed_string = hashObj.hexdigest()
      return hashed_string
   
   def get_registered_semesters(self, stdID):
      select_query = "SELECT semester FROM module_details WHERE StdID = %s"
      self.cursor.execute(select_query, [stdID])
      return {row[0] for row in self.cursor.fetchall()}


   def insert_grade(self, stdID, mod_code, year, semester, grade_point):
      insert_query = """
         INSERT INTO module_details (StdID, modulecode, year, semester, gradepoints)
         VALUES (%s, %s, %s, %s, %s)
      """
      self.cursor.execute(insert_query, (stdID, mod_code, year, semester, grade_point))
      self.connector.commit()
      print("Record inserted successfully into module_details table")


   def get_module_details(self, stdID):
      select_query = """
         SELECT gradepoints, semester 
         FROM module_details WHERE StdID = %s
      """
      self.cursor.execute(select_query, [stdID])
      return self.cursor.fetchall()
   
   def get_singleGP_byStdID(self, stdID, module_code):
      select_query = """
         SELECT gradepoints
         FROM module_details 
         WHERE StdID = %s and modulecode = %s
      """
      self.cursor.execute(select_query, [stdID, module_code])
      return self.cursor.fetchone()[0]
   
   def get_GP_byStdID(self, stdID, semester=1):
      grade_points = []
      select_query = """
         SELECT gradepoints
         FROM module_details 
         WHERE StdID = %s and semester = %s
      """
      self.cursor.execute(select_query, [stdID, semester])

      result = self.cursor.fetchall()
      for grade_point in result:
         grade_points.append(grade_point[0])
      
      return grade_points

   
   def get_credits_byStdID(self, stdID: int, semester:int=1) -> list:
      credits = []
      select_query = """
         SELECT modulecode 
         FROM module_details 
         WHERE StdID = %s and semester = %s
      """   
      self.cursor.execute(select_query, [stdID, semester])
      for module in self.cursor.fetchall():
         module_code = module[0]
         credit = self.get_module_credit(module_code)[0]
         credits.append(credit)
      
      return credits


   def get_module_credit(self, module_code: str):
      select_query = """
         SELECT credits FROM modules WHERE modulecode = %s
      """
      self.cursor.execute(select_query, [module_code])
      return self.cursor.fetchone()
   
   
   def get_module_per_semester(self, stdID, semester=1):
      select_query = """
         SELECT gradepoints, semester, modulecode
         FROM module_details WHERE StdID = %s and semester = %s
      """
      self.cursor.execute(select_query, [stdID, semester])
      return self.cursor.fetchall()

   def insert_modules(self, module, modulecode, credits):
      insert_query = "INSERT INTO modules VALUES (%s, %s, %s)"

      self.cursor.execute(insert_query, (module, modulecode, credits))
      self.connector.commit()
      print("module was inserted successfully into module table")

   
   def delete_module(self, modulecode):
      select_query = "DELETE FROM modules WHERE modulecode = %s"
      
      self.cursor.execute(select_query, (modulecode,))
      self.connector.commit()
      print("Module was deleted successfully from module table")

   def create_staff(self, staff):
      insert_query = "INSERT INTO staff VALUES (%s, %s, %s, %s, %s, %s)"
      values = staff.get_staff_details()
      self.cursor.execute(insert_query, values)

      insert_query = "INSERT INTO staff_authenticaion VALUES(%s, %s)"
      values = staff.get_staff_credentials()
      values[1] = Database.__hash(values[1])
      self.cursor.execute(insert_query, values)

      self.connector.commit()
      print(f"Staff with ID {staff.id} added successfully.")

   def read_staff(self):
      self.cursor.execute("SELECT * FROM staff")
      return self.cursor.fetchall()

   def get_staff_byID(self, staffID):
      sql_select_query = "SELECT * FROM staff WHERE staffID = %s"
      
      self.cursor.execute(sql_select_query, (staffID,))
      return self.cursor.fetchall()

   def delete_staff(self, staffID):
      sql_select_query = "DELETE FROM staff WHERE staffID = %s"
      
      self.cursor.execute(sql_select_query, (staffID,))
      self.connector.commit()
      print(f"Student with ID {staffID} deleted successfully.")

   def get_all_students(self):
      sql_select_Query = "SELECT * FROM students"
      self.cursor.execute(sql_select_Query)
      return self.cursor.fetchall()

   def get_student_byId(self, stdID):
      sql_select_query = "SELECT * FROM students WHERE stdID = %s"
      self.cursor.execute(sql_select_query, (stdID,))
      return self.cursor.fetchall()

   def create_student(self, student):
      insert_query = """
            INSERT INTO students VALUES (%s, %s, %s, %s, %s)
        """
      values = student.get_student_details()
      self.cursor.execute(insert_query, values)

      insert_query = """
         INSERT INTO student_authentication VALUES (%s, %s)
      """
      values = student.get_student_credentials()
      values[1] = Database.__hash(values[1])
      self.cursor.execute(insert_query, values)
      self.connector.commit()

      print(f"Student with ID {student.id} added successfully.")

   def delete_student(self, stdID):
      # remove from student_authentication first
      delete_query = "DELETE FROM student_authentication WHERE stdID = %s"
      self.cursor.execute(delete_query, (stdID,))
      delete_query = "DELETE FROM students WHERE stdID = %s"
      self.cursor.execute(delete_query, (stdID,))
      self.connector.commit()
      print(f"Student with ID {stdID} deleted successfully.")

   def lookupUser(self, ID, password, IDType="staffID", table="staff_authentication"):
      select_query = f"SELECT password FROM {table} WHERE {IDType} = %s"
      self.cursor.execute(select_query, [ID])
      result = self.cursor.fetchone()

      if result:
         hashed_password = Database.__hash(password)
         if result[0] == hashed_password:
            return True

      if table != "student_authentication":
         table = "student_authentication"
         return self.lookupUser(ID, password, "StdID", table)
      
      return False
   