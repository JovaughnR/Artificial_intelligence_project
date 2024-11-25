"""@authors: Shamar Bennett and Jovaughn Rose"""

import mysql.connector
import hashlib 
from person import Student

def hash_string(string):
   return hashlib.sha256(string.encode()).hexdigest()

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
   
   def get_registered_semesters(self, usrID, year):
      select_query = """
         SELECT semester 
         FROM module_details
           WHERE usrID = %s and year = %s
      """
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(select_query, [usrID, year])
         return {row[0] for row in cursor.fetchall()}


   def insert_grade(self, mod_code, module, usrID, year, semester, grade_point):
      insert_query = """
         INSERT INTO module_details (modulecode, module, usrID, year, semester, gradepoints)
         VALUES (%s, %s, %s, %s, %s, %s)
      """
      try:
         with self.connector.cursor(buffered=True) as cursor:
               cursor.execute(
                  insert_query, 
                  (mod_code, module, usrID, year, semester, grade_point)
               )
               self.connector.commit()
               return True  # Explicitly return True on success
      except mysql.connector.Error as err:
         print(f"Error: {err}")  # Log the error message for debugging
         self.connector.rollback()  # Roll back in case of error
         return False  # Explicitly return False on failure

   def get_module_details(self, usrID):
      select_query = """
         SELECT gradepoints, semester 
         FROM module_details WHERE usrID = %s
      """
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(select_query, [usrID])
         return cursor.fetchall()
   
   def get_records_ByYear(self, usrID, year):
      query = """
         select gradepoints, semester
         from module_details where
         usrID = %s and year = %s
      """
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(query, (usrID, year))
         return cursor.fetchall()
   
   def get_singleGP_byStdID(self, usrID, module_code):
      select_query = """
         SELECT gradepoints
         FROM module_details 
         WHERE usrID = %s and modulecode = %s
      """
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(select_query, [usrID, module_code])
         return cursor.fetchone()[0]
   
   def get_GP_Credit(self, usrID, semester, year):
      grade_points, credits = [], []
      query = """
         select gradepoints, modulecode 
         from module_details 
         where usrID = %s and semester = %s and year = %s"""
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(query, [usrID, semester, year])
         result = cursor.fetchall()
         for gp, mod in result:
            grade_points.append(gp)
            cred = self.get_module_credit(mod)[0]
            credits.append(cred)
         
         return grade_points, credits

   
   def get_credits_byID(self, usrID, semester, year) -> list:
      credits = []
      select_query = """
         SELECT modulecode 
         FROM module_details 
         WHERE usrID = %s and semester = %s and year = %s
      """   
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(select_query, [usrID, semester, year])
         for module in cursor.fetchall():
            module_code = module[0]
            credit = self.get_module_credit(module_code)[0]
            credits.append(credit)
         
         return credits


   def get_module_credit(self, module_code: str):
      select_query = """
         SELECT credits FROM modules WHERE modulecode = %s
      """
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(select_query, [module_code])
         return cursor.fetchone()
   
   
   def get_module_per_semester(self, usrID, semester=1):
      select_query = """
         SELECT gradepoints, semester, modulecode
         FROM module_details WHERE usrID = %s and semester = %s
      """
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(select_query, [usrID, semester])
         return cursor.fetchall()
      
   
   def isRegisteredForCourses(self, id):
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(
            "select * from module_details where usrID = %s", (id,))
      
         result = cursor.fetchone()
         return result
      
   def get_student_records(self, usrID, year=None):
      with self.connector.cursor(buffered=True) as cursor:
         if not year:
            cursor.execute("""
               select modulecode, module, semester, gradepoints
               from module_details where usrID = %s """, (usrID,))
         else:
            cursor.execute("""
               select modulecode, module, semester, gradepoints
               from module_details where usrID = %s and year = %s
               """, (usrID, year))

         return cursor.fetchall()


   def insert_module(self, module, modulecode, credits):
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(
            "insert into modules values (%s, %s, %s)", 
            (module, modulecode, credits)
         )
         self.connector.commit()
         return True

   def delete_module(self, modulecode):
      select_query = "DELETE FROM modules WHERE modulecode = %s"
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(select_query, (modulecode,))
         self.connector.commit()
         return True
   

   def create_staff(self, staff): # Tested
      status = self.validIDentry(staff.id)
      if status:
         with self.connector.cursor(buffered=True) as cursor:
            cursor.execute(
               "insert into staff values (%s, %s, %s, %s, %s, %s)",
               staff.get_details()
            )
            return self.connector.commit() == None

      raise ValueError("User ID is not registerd")
   
   def save_user_credentials(self, ID, passwd, type): # Tested
      if not self.validIDentry(ID):
         passwd = hash_string(passwd)
         with self.connector.cursor(buffered=True) as cursor:
            cursor.execute(
               "insert into user_auth values (%s, %s, %s)",
               (ID, passwd, type)
            )
            self.connector.commit()
            return True
      return False
      

   def read_staff(self): # Tested
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute("select * from staff")
         return self.cursor.fetchall()

   def delete_staff(self, usrID): # Tested
      self.delete_user_credentials(usrID)
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(
            "delete from staff where usrID = %s", (usrID,))
         return self.connector.commit() == None

   def get_all_students(self): # Tested
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute("select * from students")
         return cursor.fetchall()

   def create_student(self, stud): # Tested
      print("Student from data base: ", stud)
      status = self.validIDentry(stud.id)
      if status:
         self.cursor.execute(
            "insert into students values (%s, %s, %s, %s, %s)", 
            stud.get_details()
         )
         self.connector.commit()
         return True

      return False

   def delete_user_credentials(self, usrID): # Tested
      self.cursor.execute(
         "delete from user_auth where usrID = %s", (usrID,)
      )

   def delete_student(self, usrID): # Tested
      self.delete_user_credentials(usrID)
      self.cursor.execute(
         "delete from students where usrID = %s", (usrID,))
      return self.connector.commit() == None

   def is_user_registered(self, usrID, passwd): # Tested
      with self.connector.cursor(buffered=True) as cursor:
         cursor.execute(
            "select * from user_auth where usrID = %s", [usrID]
         )
         result = cursor.fetchone()
         print(result)
         if result:
            hash_passwd = hash_string(passwd)
            print(hash_string(result[1]))
            if result[1] == hash_passwd:
               return (True, result[2])

         return False   

   def get_user_byID(self, usrID): # Tested
      """returns user by the given `ID`"""
      def find_user(type):
         """"""
         with self.connector.cursor(buffered=True) as cursor:
            cursor.execute(
               f"select * from {type} where usrID = %s", (usrID,))
            res = cursor.fetchone()
            return res if res else None
      
      user = find_user("students")
      return user if user else find_user("staff")

   def validIDentry(self, usrID): # Tested
      """Checks the database if the given ID number does not exist"""
      def check(table):
         with self.connector.cursor(buffered=True) as cursor:
            cursor.execute(
               f"select * from {table} where usrID = %s", (usrID,))
            return cursor.fetchone() == None
      return check("staff") if check("students") else False



# db = Database(
#    host="localhost", 
#    user="root", 
#    password="", 
#    db="ai_project"
# )

# status  = db.validIDentry(2111876)
# print(status)


# status = db.validIDentry(2111821)
# print(status)

# details = ('CS113', 'Cloud Computing', 2111878, '2022', 1, 3.4)
# resut = db.insert_grade(*details)
# print(resut)



# res = db.isRegisteredForCourses(1245981)
# print(res)

# print(db.get_all_students())

# result = db.get_all_module_details('2024')
# print(result)


# records = db.get_records_ByYear(2111876, '2024')
# print(records)

# records = db.get_records_ByYear(2111876, '2025')
# print(records)

# print(db.get_GP_Credit(2111876, 1, '2024'))
# print(db.get_GP_Credit(2111876, 2, '2024'))

# records = db.get_student_records(2111876)
# if records:
#    for record in records:
#       print(record)
# else:
#    print(records == [])

# stud = Student(
#    2111821, "Jamie", "Stewart", 
#    "jovaughnstewart@gmail.com", 
#    "Computer Science"
# )
# # print(db.getUserByID(2111876))
# status = db.create_student(stud)
# print("Student Created Status:", status)

# result = db.is_user_registered(1245970, "iamtired54")
# print("Result", result)

# user = db.get_user_byID(1245120)
# print("User:", user)
# user = db.get_user_byID(2111876)
# print("User:", user)
# user = db.get_user_byID(1245989)
# print("User:", user)
# print(db.get_all_students())
# deletedStatus = db.delete_student(1245989)
# print("Deleted Status:",deletedStatus)

# userFound = db.look_up_user(2111876, "jonjo2123")
# print("User found:", userFound)

# status = db.validateIDEntry(2111876)
# print("Status:", status)
# status = db.validateIDEntry(1245910)
# print("Status:", status)
# status = db.validateIDEntry(2111873)
# print("Status:", status)
# print()

# %%
