class Person:
    def __init__(self, ID, first_name, last_name, email):
        """
        Initialize the common attributes for both Student and Staff.
        """
        self.id = ID        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

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
    def __init__(self, ID, first_name, last_name, email, programme):
        """
        Initialize the student with the provided attributes.
        """
        super().__init__(ID, first_name, last_name, email)  # Initialize the parent class
        self.programme = programme
        self.type = "student"

    def __str__(self):
        """
        Return a string representation of the student.
        """
        return f"{super().__str__()}, Student ID: {self.id}, Programme: {self.programme}"

    def update_password(self, new_password):
        """
        Update the password for the student. 
        """
        self.password = new_password
        print(f"Password updated for student ID: {self.id}")

    def get_details(self) -> tuple:
        """
        Returns a tuple of current student details.
        """
        return (
            self.id, self.first_name, 
            self.last_name, self.email, 
            self.programme
        )
   

class Staff(Person):
    def __init__(self, ID, first_name, last_name, email):
        """
        Initialize the staff with the provided attributes.
        """
        super().__init__(ID, first_name, last_name, email)  # Initialize the parent class
        self.type = "staff"

    def __str__(self):
        """
        Return a string representation of the staff member.
        """
        return f"{super().__str__()}, Staff ID: {self.id}, Type: {self.staff_type}, School: {self.school}"


    def get_details(self) -> tuple:
        """
        returns the details for the current staff member
        """
        return (
            self.id, self.first_name, 
            self.last_name, self.email, 
        )
    

# info = [2111876, "Jovaughn", "Rose", "jovaughnrose4@gmail.com", "jov83b$1", "Computer Science"]
# student = Student(*info)
# print(student.get_credentials())