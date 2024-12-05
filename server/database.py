import time
import psycopg2
from psycopg2 import OperationalError
import hashlib

def hash_string(string):
    """Hashes a given string using SHA-256."""
    return hashlib.sha256(string.encode()).hexdigest()


class Database:
   def __init__(self, host, user, password, database, max_retries=5, retry_delay=2):
      self.host = host
      self.user = user
      self.password = password
      self.database = database
      self.connector = None
      self.cursor = None
      self.max_retries = max_retries
      self.retry_delay = retry_delay
      self.__connect()

   def __connect(self):
      """Initialize the connection to the database with reconnection logic."""
      retries = 0
      while retries < self.max_retries:
         try:
            self.connector = psycopg2.connect(
               host=self.host,
               user=self.user,
               password=self.password,
               database=self.database
            )
            print("Database connection established.")
            self.cursor = self.connector.cursor()
            return  # Connection successful, exit loop
         except OperationalError as e:
               print(f"Error connecting to the database: {e}. Retrying in {self.retry_delay} seconds...")
               time.sleep(self.retry_delay)
               retries += 1

      raise ConnectionError("Failed to connect to the database after multiple attempts.")

   def reconnect(self):
      """Reconnect to the database if the connection is lost."""
      if self.connector and not self.connector.closed:
         return  # Already connected

      print("Re-establishing database connection...")
      self.__connect()

   def __handle_error(self, error, rollback=True):
      """Logs errors, attempts reconnection, and rolls back changes if required."""
      print(f"Database Error: {error}")
      if rollback:
         try:
            self.connector.rollback()
         except Exception as e:
            print(f"Error during rollback: {e}")
         finally:
            self.connector.close() 

      if isinstance(error, psycopg2.Error):
         self.reconnect()

   def execute_query(self, query, params=None):
      """Execute a SQL query with automatic reconnection logic."""
      try:
         self.reconnect()  # Ensure the connection is alive
         self.cursor.execute(query, params)
         return self.cursor.fetchall()
      except psycopg2.Error as e:
         self.__handle_error(e)
         return None

   # Other methods (e.g., insert_grade, get_module_details, etc.) can be similarly updated

   def get_registered_semesters(self, usrID, year):
      """Retrieve semesters a user is registered for in a given year."""
      query = """
         SELECT semester 
         FROM module_details
         WHERE usrID = %s AND year = %s
      """
      try:
         self.cursor.execute(query, (usrID, year))
         return {row[0] for row in self.cursor.fetchall()}
      except OperationalError as e:
         self.__handle_error(e)
         return set()

   def insert_grade(self, mod_code, module, usrID, year, semester, grade_point):
      """Insert grade information into the database."""
      query = """
         INSERT INTO module_details (modulecode, module, usrID, year, semester, gradepoints)
         VALUES (%s, %s, %s, %s, %s, %s)
      """
      try:
         self.cursor.execute(query, (mod_code, module, usrID, year, semester, grade_point))
         self.connector.commit()
         return True
      except OperationalError as e:
         self.__handle_error(e)
         return False
      
   def insert_module(self, module_name, module_code, credits):
      """
      Inserts a new module into the database.

      Args:
         module_name (str): The name of the module.
         module_code (str): The unique code of the module.
         credits (int): The credit value of the module.

      Returns:
         bool: True if the module was inserted successfully, False otherwise.
      """
      try:
         insert_query = """
               INSERT INTO modules (module, modulecode, credits)
               VALUES (%s, %s, %s)
         """
         self.cursor.execute(insert_query, (module_name, module_code, credits))
         self.connector.commit()
         print(f"Module '{module_name}' with code '{module_code}' inserted successfully.")
         return True
      except psycopg2.IntegrityError as e:
         print(f"Integrity error: Module with code '{module_code}' might already exist. {e}")
         return False
      except psycopg2.Error as e:
         print(f"Database error while inserting module '{module_name}': {e}")
         return False
      except Exception as e:
         print(f"Unexpected error while inserting module '{module_name}': {e}")
         return False
    

   def get_module_details(self, usrID):
      """Retrieve all module details for a specific user."""
      query = """
         SELECT gradepoints, semester 
         FROM module_details WHERE usrID = %s
      """
      try:
         self.cursor.execute(query, (usrID,))
         return self.cursor.fetchall()
      except OperationalError as e:
         self.__handle_error(e)
         return []
      
   def get_records_by_year(self, usrID, year=None):
      """
      Retrieve records for a user by year. If no year is specified, retrieve records for all years.
      Args:
         usrID (int): The user's ID.
         year (str, optional): The year to filter records. Defaults to None.

      Returns:
         list: A list of tuples containing grade points and semesters.
      """
      try:
         if year:
            query = """
                  SELECT modulecode, module, semester, gradepoints
                  FROM module_details
                  WHERE usrID = %s AND year = %s
            """
            self.cursor.execute(query, (usrID, year))
         else:
            query = """
                  SELECT modulecode, module, semester, gradepoints
                  FROM module_details
                  WHERE usrID = %s
            """
            self.cursor.execute(query, (usrID,))
         return self.cursor.fetchall()
      except psycopg2.Error as e:
         print(f"Database error while retrieving records: {e}")
         return []
      except Exception as e:
         print(f"Unexpected error while retrieving records: {e}")
         return []


   def get_single_grade_point(self, usrID, module_code):
      """Retrieve a specific grade point by user ID and module code."""
      query = """
         SELECT gradepoints
         FROM module_details
         WHERE usrID = %s AND modulecode = %s
      """
      try:
         self.cursor.execute(query, (usrID, module_code))
         result = self.cursor.fetchone()
         return result[0] if result else None
      except OperationalError as e:
         self.__handle_error(e)
         return None
      
   def get_GP_Credit(self, usrID, semester, year):
      """
      Retrieve grade points and credits for a user's modules in a specific semester and year.

      Args:
         usrID (int): The user ID of the student.
         semester (int): The semester number (e.g., 1 or 2).
         year (str): The academic year (e.g., "2024").

      Returns:
         tuple: Two lists - grade points and credits. Returns empty lists in case of an error or no data.
      """
      grade_points = []
      credits = []

      query = """
         SELECT gradepoints, modulecode
         FROM module_details
         WHERE usrID = %s AND semester = %s AND year = %s
      """
      try:
         self.cursor.execute(query, (usrID, semester, year))
         result = self.cursor.fetchall()

         for grade_point, module_code in result:
            grade_points.append(grade_point)
            credit = self.get_module_credit(module_code)
            if credit is not None:  # Ensure credit retrieval is successful
               credits.append(credit)
            else:
               print(f"Warning: Could not retrieve credits for module {module_code}.")

         return grade_points, credits
      except psycopg2.Error as e:
         print(f"Error retrieving grade points and credits: {e}")
         return [], []

   def get_credits_by_id(self, usrID, semester, year):
      """Retrieve credits for all modules of a user in a specific semester and year."""
      query = """
         SELECT modulecode
         FROM module_details
         WHERE usrID = %s AND semester = %s AND year = %s
      """
      try:
         self.cursor.execute(query, (usrID, semester, year))
         module_codes = [row[0] for row in self.cursor.fetchall()]
         credits = [self.get_module_credit(module_code) for module_code in module_codes]
         return credits
      except OperationalError as e:
         self.__handle_error(e)
         return []

   def get_module_credit(self, module_code):
      """Retrieve the credit value of a module by its code."""
      query = """
         SELECT credits
         FROM modules
         WHERE modulecode = %s
      """
      try:
         self.cursor.execute(query, (module_code,))
         result = self.cursor.fetchone()
         return result[0] if result else None
      except OperationalError as e:
         self.__handle_error(e)
         return None
      

   def is_user_registered(self, usrID, passwd):
      """
      Checks if a user is registered with the provided credentials.

      Args:
         usrID (int): The user's ID.
         passwd (str): The password to verify.

      Returns:
         tuple: (True, user_type) if credentials match and the user exists,
                  (False, None) otherwise.
      """
      try:
        # Query to fetch user details based on ID
         self.cursor.execute(
            "SELECT password, type FROM user_auth WHERE usrID = %s",
            (usrID,)
         )
         result = self.cursor.fetchone()

         # If no user is found, return False
         if not result:
               print(f"No user found with ID {usrID}.")
               return False

         # Unpack results
         stored_password, user_type = result

         # Hash the provided password
         hashed_password = hash_string(passwd)

         # Compare hashed password with stored password
         if stored_password == hashed_password:
               print(f"User {usrID} successfully authenticated as {user_type}.")
               return True, user_type
         else:
               print(f"Password mismatch for user {usrID}.")
               return False
      except psycopg2.Error as e:
         print(f"Database error while verifying user {usrID}: {e}")
         return False

      except Exception as e:
         print(f"Unexpected error while verifying user {usrID}: {e}")
         return False
      
   def get_user_byID(self, usrID):
      """
      Retrieves user information based on their ID.
      Args:
         usrID (int): The ID of the user to retrieve.
      Returns:
         tuple: A tuple containing the user's details if found, otherwise None.
      """
      try:
         def find_user(table):
            query = f"SELECT * FROM {table} WHERE usrID = %s"
            self.cursor.execute(query, (usrID,))
            result = self.cursor.fetchone()
            return result if result else None

         # Attempt to find the user in the students table
         student = find_user("students")
         return student if student else find_user("staff")

      except psycopg2.Error as e:
         print(f"Database error while retrieving user {usrID}: {e}")
         return None

      except Exception as e:
         print(f"Unexpected error while retrieving user {usrID}: {e}")
         return None


   def is_registered_for_courses(self, usrID):
      """Check if a user is registered for any courses."""
      query = "SELECT * FROM module_details WHERE usrID = %s"
      try:
         self.cursor.execute(query, (usrID,))
         return self.cursor.fetchone() is not None
      except OperationalError as e:
         self.__handle_error(e)
         return False

   def create_staff(self, staff):
      """Create a new staff member."""
      if self.valid_id_entry(staff.id):
         try:
            self.cursor.execute(
               """INSERT INTO staff (usrID, fname, lname, email) 
               VALUES (%s, %s, %s, %s)""",
               staff.get_details()
            ) 
            self.connector.commit()
            self.save_credentials(staff.id, '', "staff")
            return True
         except OperationalError as e:
               self.__handle_error(e)
      return False

   def save_credentials(self, ID, passwd, user_type):
      """Save user credentials."""
      hashed_password = hash_string(passwd)
      query = """
         INSERT INTO user_auth (usrID, password, type)
         VALUES (%s, %s, %s)
      """
      try:
         self.cursor.execute(query, (ID, hashed_password, user_type))
         self.connector.commit()
      except OperationalError as e:
         self.__handle_error(e)

   def create_student(self, student):
      """
      Create a new student entry in the database.

      Args:
         student (Student): An instance of the Student class containing student details.

      Returns:
         bool: True if the student is successfully created, False otherwise.
      """
      try:
         # Check if the student ID already exists
         if not self.valid_id_entry(student.id):
            print(f"Student ID {student.id} already exists. Cannot create student.")
            return False

         # Insert student details into the 'students' table

         self.cursor.execute(
            """
            INSERT INTO students (usrID, firstname, lastname, email, programme)
            VALUES (%s, %s, %s, %s, %s)
            """,
            student.get_details()
         )
         self.connector.commit()

         # Save user credentials for the student
         self.save_credentials(student.id, "", "student")
         print(f"Student ID {student.id} created successfully.")
         return True

      except psycopg2.Error as e:
         print(f"Database error while creating student: {e}")
         self.connector.rollback()
         return False

      except Exception as e:
         print(f"Unexpected error while creating student: {e}")
         return False

   def get_all_students(self):
      """
      Retrieve all student records from the database.

      Returns:
         list: A list of tuples, where each tuple contains student details.
               Returns an empty list if no students are found or an error occurs.
      """
      try:
         query = "SELECT * FROM students"
         self.cursor.execute(query)
         return self.cursor.fetchall()
      except psycopg2.Error as e:
         print(f"Database error while retrieving students: {e}")
         return []
      except Exception as e:
         print(f"Unexpected error while retrieving students: {e}")
         return []

   def update_password(self, ID, passwd):
      """Update the password for a user."""
      hashed_password = hash_string(passwd)
      query = """
         UPDATE user_auth SET password = %s 
         WHERE usrID = %s
      """
      try:
         self.cursor.execute(query, (hashed_password, ID))
         self.connector.commit()
         return True
      except OperationalError as e:
         self.__handle_error(e)
         return False

   def valid_id_entry(self, usrID):
      """Check if a user ID does not exists in the database."""
      def check_table(table):
         query = f"SELECT * FROM {table} WHERE usrID = %s"
         try:
            self.cursor.execute(query, (usrID,))
            return self.cursor.fetchone() is None
         except OperationalError as e:
               print("error")
               self.__handle_error(e)
               return False
      return check_table("staff") if check_table("students") else False
   
   def verify_email_id(self, usrID, email):
      def check_table(table):
         query = f"SELECT usrID FROM {table} WHERE usrID = %s AND email = %s"
         self.cursor.execute(query, (usrID, email))
         return self.cursor.fetchone() is not None
      try:
         result = check_table("students")
         return result if result else check_table("staff")
      except OperationalError as e:
         self.__handle_error(e)
         return False
