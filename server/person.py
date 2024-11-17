class Person:
    def __init__(self, ID, first_name, last_name, email, password):
        """
        Initialize the common attributes for both Student and Staff.
        """
        self.id = ID        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __str__(self):
        """
        Return a string representation of the person.
        """
        return f"Name: {self.first_name} {self.last_name}, Email: {self.email}"

    def update_email(self, new_email):
        """
        Update the email for the person.
        """
        self.email = new_email
        print(f"Email updated for {self.first_name} {self.last_name}")

    def full_name(self):
        """
        Return the full name of the person.
        """
        return f"{self.first_name} {self.last_name}"

# Now, Student and Staff will inherit from the Person class

class Student(Person):
    def __init__(self, ID, first_name, last_name, email, password, programme):
        """
        Initialize the student with the provided attributes.
        """
        super().__init__(ID, first_name, last_name, email, password)  # Initialize the parent class
        self.programme = programme

    def __str__(self):
        """
        Return a string representation of the student.
        """
        return f"{super().__str__()}, Student ID: {self.id}, Password: {self.password} Programme: {self.programme}"

    def update_password(self, new_password):
        """
        Update the password for the student. 
        """
        self.password = new_password
        print(f"Password updated for student ID: {self.id}")

    def get_student_details(self) -> tuple:
        """
        Returns a tuple of current student details.
        """
        return (
            self.id, self.first_name, 
            self.last_name, self.email, 
            self.programme
        )
   
    def get_student_credentials(self):
       """
       Returns the student authentication details.
       """
       return [
           self.id, self.password
       ]

class Staff(Person):
    def __init__(self, ID, first_name, last_name, email, password, staff_type, school):
        """
        Initialize the staff with the provided attributes.
        """
        super().__init__(ID, first_name, last_name, email, password)  # Initialize the parent class
        self.staff_type = staff_type
        self.school = school

    def __str__(self):
        """
        Return a string representation of the staff member.
        """
        return f"{super().__str__()}, Staff ID: {self.id}, Type: {self.staff_type}, School: {self.school}"

    def update_staff_type(self, new_type):
        """
        Update the staff type (e.g., 'Lecture', 'Admin').
        """
        self.staff_type = new_type
        print(f"Staff type updated for staff ID: {self.id}")

    def get_staff_details(self) -> tuple:
        """
        returns the details for the current staff member
        """
        return (
            self.id, self.first_name, 
            self.last_name, self.email, 
            self.staff_type, self.school
        )
    
    def get_staff_credentials(self) -> tuple:
        """
        Returns the current staff member login credentials
        """
        return [
            self.id, self.password
        ]

info = [2111876, "Jovaughn", "Rose", "jovaughnrose4@gmail.com", "jov83b$1", "Computer Science"]
student = Student(*info)
print(student)