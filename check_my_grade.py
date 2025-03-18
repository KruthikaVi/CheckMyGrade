import os
from time import time
import shutil
import getpass
import csv
from encdyc import TextSecurity


##    ====================== LoginUser Class =======================
##    Class to login, signup and delete Login records.
##    ============================================================
class LoginUser:
    def __init__(self, email_address=None, password=None):
        self.cipher = TextSecurity(4)
        self.email_address = email_address
        self.password = password
        self.users = []
        self.load_login_data()

    def load_login_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "login.csv")
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                self.users = list(reader)[1:]
        except Exception as e:
            print(f"Error reading the user info {str(e)}")

    def save_login_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "login.csv")
            with open(file_path, "w") as file:
                writer = csv.writer(file)
                writer.writerow(["User_id", "Password", "Role"])
                writer.writerows(self.users)
        except Exception as e:
            print(f"Error reading the user info {str(e)}")

    def create_user(self, email_address, password, role):
        try:
            for user in self.users:
                if user[0] == email_address:
                    return f"This user {email_address} is already registered, try different email!"
            password = self.cipher.encrypt(password)
            if role not in ["student", "professor"]:
                return "Only students or professors are allowed to register"
            new_user = [email_address, password, role]
            self.users.append(new_user)
            self.save_login_data()
            return "Successfully registered user, login to the application"
        except Exception as e:
            print(f"Error creating the user {str(e)}")

    def login(self, email_address, password):
        try:
            for user in self.users:
                if user[0] == email_address and self.cipher.decrypt(user[1]) == password:
                    print(f"Login Successful!! Role: {user[2]}")
                    return True, user[2]
            print("Invalid login attempt")
            return False, None
        except Exception as e:
            print(f"Error while logging in {str(e)}")

    def logout(self):
        """Logout of the system"""
        return False

    def delete_record(self, email_address):
        """Deletes user details"""
        try:
            self.users = [user for user in self.users if user[0] != email_address]
            self.save_login_data()
            self.load_login_data()
            return "User removed successfully!"
        except Exception as e:
            print(f"Error deleting the user record {str(e)}")

    def change_password(self, email_address, old_password):
        try:
            for i, user in enumerate(self.users):
                if (
                    user[0] == email_address
                    and self.cipher.decrypt(user[1]) == old_password
                ):
                    new_password = getpass.getpass("Enter new password: ")
                    self.users[i][1] = self.cipher.encrypt(new_password)
                    self.save_login_data()
                    return "Password changed successfully!!!"
            return "Incorrect email or password"
        except Exception as e:
            print(f"Error changing the user password {str(e)}")


##    ====================== Student Class =======================
##    Class to add, update, delete and display student records.
##    ============================================================
class Student:
    def __init__(
        self,
        email_address=None,
        first_name=None,
        last_name=None,
        course_id=None,
        grade=None,
        marks=None,
    ):
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.course = course_id
        self.grade = grade
        self.marks = marks
        self.students = []
        self.load_student_data()
        self.grades_manager = Grades()

    def load_student_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "student.csv")
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                self.students = list(reader)[1:]
        except Exception as e:
            print(f"Error reading the student info {str(e)}")

    def add_new_student(self, email_address, first_name, last_name, course_id, marks=None):
        try:
            self.login_manager = LoginUser()
            self.course_manager = Course()
            start_process = time()
            student_info = []
            for student in self.students:
                if student[0] == email_address and student[3] == course_id:
                    return f"Record for student {email_address} for the course {course_id} already exists, update the marks instead!"
            user_exists = False
            for user in self.login_manager.users:
                if user[0] == email_address:
                    student_info.append(email_address)
                    user_exists = True
                    break
            if not user_exists:
                return f"User is not Signed up in the system, exit and signup for student: {email_address}"
            student_info.append(first_name)
            student_info.append(last_name)
            course_exists = False
            for course in self.course_manager.courses:
                if course[0] == course_id:
                    student_info.append(course_id)
                    course_exists = True
                    break
            if not course_exists:
                return f"Could not find the course {course_id} in the database, register new course."
            marks = int(marks) if marks else marks
            if marks:
                grade = self.grades_manager.add_grade(marks)
            else:
                grade = None
            student_info.append(grade)
            student_info.append(marks)
            self.students.append(student_info)
            self.save_data()
            self.load_student_data()
            end_process = time()
            # print(f"Time taken to add new student is {end_process - start_process} Seconds")
            return f"Successfully added student info for {email_address}"
        except Exception as e:
            print(f"Error adding new student {str(e)}")

    def delete_student(self, email_address):
        """Deletes all the records for a given student"""
        try:
            start_process = time()
            self.students = [
                student for student in self.students if student[0] != email_address
            ]
            self.save_data()
            self.load_student_data()
            end_process = time()
            #    print(f"Time taken to delete student is {end_process - start_process} Seconds")
            return f"Student {email_address} deleted successfully!"
        except Exception as e:
            print(f"Error deleting student {str(e)}")

    def check_my_grades(self, email_address, course_id=None):
        """Check the grades of a student"""
        try:
            start_process = time()
            record = [
                student for student in self.students
                if student[0] == email_address and (course_id is None or student[3] == course_id)]
            if record:
                record = sorted(record, key=lambda rec: rec[5], reverse=True)
                end_process = time()
                print(
                    f"Time taken to check grade is {end_process - start_process} Seconds"
                )
                return record
            else:
                return f"Could not find any record for student {email_address}"
        except Exception as e:
            print(f"Error fetching student grade{str(e)}")

    def update_student_record(self, email_address, course_id, new_marks):
        """Updates the students record with marks and grade for given course"""
        try:
            start_process = time()
            for student in self.students:
                if student[0] == email_address and student[3] == course_id:
                    student[4] = self.grades_manager.add_grade(int(new_marks))
                    student[5] = int(new_marks)
                    self.save_data()
                    self.load_student_data()
                    end_process = time()
                    print(
                        f"Time taken to update student record is {end_process - start_process} Seconds"
                    )
                    return "Updated new marks successfully!"
            return f"Could not find the student {email_address}, create student before updating"
        except Exception as e:
            print(f"Error updating the student record {str(e)}")

    def check_my_marks(self, email_address, course_id=None):
        """Check the marks of a student"""
        try:
            start_process = time()
            record = [
                student for student in self.students
                if student[0] == email_address and (course_id is None or student[3] == course_id)]
            if record:
                record = sorted(record, key=lambda rec: rec[4], reverse=True)
                end_process = time()
                print(
                    f"Time taken to check marks of student is {end_process - start_process} Seconds"
                )
                return record
            else:
                return f"Could not find any record for student {email_address}"
        except Exception as e:
            print(f"Error fetching student marks{str(e)}")

    def display_record(self, email_address=None):
        """Display  record of all/selected students"""
        try:
            start_process = time()
            if email_address:
                students = [
                    student for student in self.students if student[0] == email_address
                ]
            else:
                students = self.students
            if students:
                reports = sorted(students, key=lambda student: student[5], reverse=True)
                end_process = time()
                print(
                    f"Time taken to display student records is {end_process - start_process} Seconds"
                )
                return reports
            else:
                "No student record to display"
        except Exception as e:
            print(f"Error displaying the user record {str(e)}")

    def save_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "student.csv")
            with open(file_path, "w") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "Email_address",
                        "First_name",
                        "Last_name",
                        "Course_id",
                        "Grades",
                        "Marks",
                    ]
                )
                writer.writerows(self.students)
        except Exception as e:
            print(f"Error reading the student info {str(e)}")

    def sort_students(self, field, reverse=False):
        try:
            start_process = time()
            result = sorted(
                self.students, key=lambda student: student[int(field)], reverse=reverse
            )
            end_process = time()
            print(
                f"Time taken to sort students info is {end_process - start_process} Seconds"
            )
            return result
        except Exception as e:
            print(f"Error sorting the student info {str(e)}")


##    ====================== Grades Class =======================
##    Class to manage and track student grades.
##    ============================================================
class Grades:
    def __init__(self, email_address=None, course_id=None, marks=None):
        self.email_address = email_address
        self.course_id = course_id
        self.marks = marks

    def add_grade(self, marks):
        """Convert to grade based on the marks"""
        try:
            self.marks = int(marks)
            if self.marks >= 90:
                grade = "A"
            elif self.marks >= 80:
                grade = "B"
            elif self.marks >= 70:
                grade = "C"
            elif self.marks >= 60:
                grade = "D"
            else:
                grade = "F"
            return grade
        except Exception as e:
            print(f"Error adding grade {str(e)}")

    def delete_grade(self, email_address, course_id):
        """Deletes Grade for a student"""
        try:
            student_manager = Student()
            for student in student_manager.students:
                if student[0] == email_address and student[3] == course_id:
                    student[4] = None
                    student[5] = None
                    student_manager.save_data()
                    student_manager.load_student_data()
                return "Grade deleted successfully"
            return "Could not find the student and course info!"
        except Exception as e:
            print(f"Error reading the professor info {str(e)}")

    def modify_grade(self, email_address,course_id,marks):
        try:
            student_manager = Student()
            return student_manager.update_student_record(email_address,course_id,marks)
        except Exception as e:
            print(f"Error modifying user grade{str(e)}")

    def display_grade_report(self, email_address=None):
        """Display Grade report of all/selected students"""
        try:
            start_process = time()
            student_manager = Student()
            if email_address:
                students = [
                    student
                    for student in student_manager.students
                    if student[0] == email_address
                ]
            else:
                students = student_manager.students
            reports = sorted(students, key=lambda student: student[5], reverse=False)
            end_process = time()
            print(
                f"Time taken to display grade report is {end_process - start_process} Seconds"
            )
            return reports
        except Exception as e:
            print(f"Error displaying the user report {str(e)}")


##    ====================== Professor Class =======================
##    Class to add, delete, display, modify professor details.
##    ============================================================
class Professor:
    def __init__(
        self, email_address=None, professor_name=None, rank=None, course_id=None
    ):
        self.email_address = email_address
        self.professor_name = professor_name
        self.rank = rank
        self.course_id = course_id
        self.professors = []
        self.load_prof_data()

    def load_prof_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "professor.csv")
            with open(file_path, "r") as prof_file:
                reader = csv.reader(prof_file)
                self.professors = list(reader)[1:]
        except Exception as e:
            print(f"Error reading the professor info {str(e)}")

    def save_prof_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "professor.csv")
            with open(file_path, "w") as file:
                writer = csv.writer(file)
                writer.writerow(["email_address", "name", "rank", "course_id"])
                writer.writerows(self.professors)
        except Exception as e:
            print(f"Error reading the student info {str(e)}")

    def professor_details(self, email_address=None):
        """Display  record of all/selected Professors"""
        try:
            start_process = time()
            if email_address:
                professors = [
                    professor
                    for professor in self.professors
                    if professor[0] == email_address
                ]
            else:
                professors = self.professors
            if professors:
                reports = sorted(
                    professors, key=lambda professor: professor[3], reverse=False
                )
                end_process = time()
                print(
                    f"Time taken to display professor is {end_process - start_process} Seconds"
                )
                return reports
            else:
                "No Professor record to display"
        except Exception as e:
            print(f"Error fetching professor details {str(e)}")

    def add_new_professor(self, email_address, name, rank, course_id):
        try:
            self.login_manager = LoginUser()
            self.course_manager = Course()
            start_process = time()
            professor_info = []
            for professor in self.professors:
                if professor[0] == email_address and professor[3] == course_id:
                    return f"Record for professor {email_address} for the course {course_id} already exists, update the professor instead!"
            user_exists = False
            for user in self.login_manager.users:
                if user[0] == email_address:
                    professor_info.append(email_address)
                    user_exists = True
                    break
            if not user_exists:
                return f"User is not Signed up in the system, exit and signup for professor: {email_address}"
            professor_info.append(name)
            professor_info.append(rank)
            course_exists = False
            for course in self.course_manager.courses:
                if course[0] == course_id:
                    professor_info.append(course_id)
                    course_exists = True
                    break
            if not course_exists:
                return f"Could not find the course {course_id} in the database, register new course."

            self.professors.append(professor_info)
            self.save_prof_data()
            end_process = time()
            # print(f"Time taken to add new professor is {end_process - start_process} Seconds")
            return f"Successfully added professor info for {email_address}"
        except Exception as e:
            print(f"Error adding new professor {str(e)}")

    def delete_professor(self, email_address):
        try:
            self.professors = [
                prof for prof in self.professors if prof[0] != email_address
            ]
            self.save_prof_data()
            return f"Professor {email_address} deleted successfully!"
        except Exception as e:
            print(f"Error deleting professor {str(e)}")

    def modify_professor_details(
        self, email_address, new_name=None, new_rank=None, new_course=None
    ):
        try:
            for prof in self.professors:
                if prof[0] == email_address:
                    if new_name:
                        prof[1] = new_name
                    if new_rank:
                        prof[2] = new_rank
                    if new_course:
                        prof[3] = new_course
                    self.save_prof_data()
                    return "professor details are updated"
            return "Professor not found"
        except Exception as e:
            print(f"Error modifying professor {str(e)}")

    def professor_course_details(self, email_address):
        """Display  record of all/selected Professors"""
        try:
            start_process = time()
            if email_address:
                professors = [
                    professor
                    for professor in self.professors
                    if professor[0] == email_address
                ]
            else:
                professors = self.professors
            if professors:
                reports = sorted(
                    professors, key=lambda professor: professor[3], reverse=False
                )
                end_process = time()
                print(
                    f"Time taken to display professor is {end_process - start_process} Seconds"
                )
                return reports
            else:
                "No Professor record to display"
        except Exception as e:
            print(f"Error fetching professor details {str(e)}")


##    ====================== Course Class =======================
##    Class to add, delete, display, modify course details.
##    ============================================================
class Course:
    def __init__(self, course_id=None, course_name=None, description=None):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.courses = []
        self.load_course_data()

    def load_course_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "course.csv")
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                self.courses = list(reader)[1:]
        except Exception as e:
            print(f"Error reading the course info {str(e)}")

    def save_course_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "course.csv")
            with open(file_path, "w") as file:
                writer = csv.writer(file)
                writer.writerow(["course_id", "course_name", "description"])
                writer.writerows(self.courses)
        except Exception as e:
            print(f"Error reading the course info {str(e)}")

    def display_courses(self, course_id=None):
        """Display  record of all/selected Courses"""
        start_process = time()
        try:
            if course_id:
                courses = [course for course in self.courses if course[0] == course_id]
            else:
                courses = self.courses
            if courses:
                reports = sorted(courses, key=lambda course: course[0], reverse=False)
                end_process = time()
                print(
                    f"Time taken to display courses is {end_process - start_process} Seconds"
                )
                return reports
            else:
                return "No Course record to display"
        except Exception as e:
            print(f"Error displaying course {str(e)}")

    def add_new_course(self, course_id, course_name, description):
        try:
            course_info = []
            for course in self.courses:
                if course[0] == course_id:
                    return f"Record for Course with course id {course_id} already exists, to modify, delete and existing and add again!"
            course_info.append(course_id)
            course_info.append(course_name)
            course_info.append(description)
            self.courses.append(course_info)
            self.save_course_data()
            return f"Course {course_id} added successfully!"
        except Exception as e:
            print(f"Error adding new course {str(e)}")

    def delete_course(self, course_id):
        try:
            self.courses = [course for course in self.courses if course[0] != course_id]
            self.save_course_data()
            return f"Course {course_id} deleted successfully!"
        except Exception as e:
            print(f"Error deleting course {str(e)}")


# Helper function to take optional input
def get_optional_input(prompt, default_value=None):
    try:
        user_input = input(f"{prompt} (default: {default_value}): ")
        return user_input if user_input else default_value
    except Exception as e:
            print(f"Error getting optional input {str(e)}")


# Helper function for display records
def print_records(data, headers=None):
    try:
        if any(isinstance(i, list) for i in data):
            # Calculate the maximum width of each column
            column_widths = []
            if headers:
                column_widths = [len(header) for header in headers]
            
            # Find the longest item in each column (headers and rows)
            for row in data:
                for i, item in enumerate(row):
                    column_widths[i] = max(column_widths[i], len(str(item)))
            
            # Print headers with dynamic column width
            header_row = " | ".join(f"{header: <{column_widths[i]}}" for i, header in enumerate(headers))
            print(header_row)
            print("-" * (sum(column_widths) + (len(column_widths) - 1) * 3))  # Separator line
            
            # Print each record with dynamic column width
            for row in data:
                print(" | ".join(f"{str(item): <{column_widths[i]}}" for i, item in enumerate(row)))
        else:
            print(data)
    except Exception as e:
        print(f"Exception in printing record {str(e)}")


def check_my_grade():
    student_manager = Student()
    login_manager = LoginUser()
    professor_manager = Professor()
    course_manager = Course()
    grades_manager = Grades()
    while True:
        columns = shutil.get_terminal_size().columns
        print("=================================".center(columns))
        print("Welcome to CheckMyGrade Application".center(columns))
        print("San Jose State University".center(columns))
        print("California,USA".center(columns))
        print("================================".center(columns))
        print("\n CheckMyGrade Main Menu:")
        print("1. Login")
        print("2. Change Password")
        print("3. Sign up")
        print("4. Exit")

        choice = input("Enter your Choice: ")
        if choice == "1":
            print("Login to the system".center(columns))
            login_manager = LoginUser()
            print("Enter login details...")
            email_address = input("Enter Email address: ")
            password = getpass.getpass("Enter your password: ")
            status, role = login_manager.login(email_address.strip(), password)
            if status:
                print("User is logged in successfully!".center(columns))
                if role == "professor":
                    while True:
                        print("=================================".center(columns))
                        print(f"Welcome to the professor portal: {email_address}".center(columns))
                        print("=================================".center(columns))
                        print("\n CheckMyGrade Main Menu:")
                        print("1. Professor details")
                        print("2. Add new professor")
                        print("3. Modify professor details")
                        print("4. Show course details for professor")
                        print("5. Delete professor")
                        print("6. Add Student")
                        print("7. Update student record")
                        print("8. Display Student records")
                        print("9. Check Student grade")
                        print("10. Check student marks")
                        print("11. Sort student record by field")
                        print("12. Delete Student")
                        print("13. Display Course")
                        print("14. Add new Course")
                        print("15. Delete Course")
                        print("16. Display grade report")
                        print("17. Add/Modify Grade for a student")
                        print("18. Delete grade for a student")
                        print("19. Logout")
                        choice = input("Enter your Choice: ")
                        if choice == "1":
                            print("Details for professor".center(columns))
                            email_address = get_optional_input("Enter email address, press enter to list all professors",)
                            records = professor_manager.professor_details(email_address)
                            print_records(records, ["Email Address","Name","Rank","Course_Id"])
                        elif choice == "2":
                            print("Add new professor".center(columns))
                            email_address = input("Enter email address for Professor: ")
                            name = input("Enter Professor name: ")
                            rank = input("Enter Professor rank: ")
                            course_id = input("Enter course id: ")
                            professor_manager=Professor()
                            print_records(professor_manager.add_new_professor(email_address,name,rank,course_id))
                        elif choice == "3":
                            print("Modify professor details".center(columns))
                            email_address = input("Enter professor email address: ")
                            new_name = get_optional_input("Enter professor name, press enter to skip: ")
                            new_rank = get_optional_input("Enter professor rank, press enter to skip: ")
                            new_course_id = get_optional_input("Enter course id, press enter to skip: ")
                            professor_manager=Professor()
                            print_records(professor_manager.modify_professor_details(email_address,new_name,new_rank,new_course_id))
                        elif choice == "4":
                             print("Course details of Professor".center(columns))
                             email_address = input("Enter Professor email address: ")
                             professor_manager=Professor()
                             records = professor_manager.professor_course_details(email_address)
                             print_records(records, ["Email Address","Name","Rank","Course_Id"])
                        elif choice == "5":
                             print("Delete Professor details".center(columns))
                             email_address = input("Enter Professor email address: ")
                             professor_manager=Professor()
                             print_records(professor_manager.delete_professor(email_address))
                        elif choice == "6":
                             print("Add student".center(columns))
                             email_address = input("Enter student's email address: ")
                             first_name = input("Enter student's first name: ")
                             last_name = input("Enter student's last name: ")
                             course_id = input("Enter student's course_id: ")
                             marks=get_optional_input("Enter student's marks (optional), press enter to skip it:  ")
                             student_manager=Student()
                             print_records(student_manager.add_new_student(email_address,first_name,last_name,course_id,marks))
                        elif choice == "7":
                             print("Update student record".center(columns))
                             student_manager=Student()
                             email_address = input("Enter student's email address: ")
                             course_id = input("Enter student's course_id: ")
                             new_marks=input("Enter new marks: ")
                             print_records(student_manager.update_student_record(email_address,course_id,new_marks))
                        elif choice == "8":
                             print("Display Student records".center(columns))
                             student_manager=Student()
                             email_address = get_optional_input("Enter student's email address, press enter to list all students: ")
                             records=student_manager.display_record(email_address)
                             print_records(records, ["Email Address","First_Name","Last_Name","Course_Id","Grade", "Marks"])
                        elif choice == "9":
                             print("Check Student grade".center(columns))
                             student_manager=Student()
                             email_address = input("Enter student's email address: ")
                             course_id = get_optional_input("Enter student's course_id, press enter to list for all courses: ")
                             records = student_manager.check_my_grades(email_address, course_id)
                             print_records(records, ["Email Address","First_Name","Last_Name","Course_Id","Grade", "Marks"])
                        elif choice == "10":
                             print("Check student marks".center(columns))
                             student_manager=Student()
                             email_address = input("Enter student's email address: ")
                             course_id = get_optional_input("Enter student's course_id, press enter to list for all courses: ")
                             records = student_manager.check_my_marks(email_address, course_id)
                             print_records(records, ["Email Address","First_Name","Last_Name","Course_Id","Grade", "Marks"])
                        elif choice == "11":
                             print("Sort student record by field".center(columns))
                             student_manager=Student()
                             field=input("Enter the field name you want to sort:\n 0 for email 1 for Firstname, 2 for Lastname, 3 for Course_id, 4 for Grades, 5 for marks")
                             reverse = input("Enter if you want the reverse sorting, 1 for Yes, 2 for No")
                             if reverse == "1":
                                records = student_manager.sort_students(int(field.strip()),True)
                             else:
                                 records = student_manager.sort_students(int(field.strip()))
                             print_records(records, ["Email Address","First_Name","Last_Name","Course_Id","Grade", "Marks"])
                        elif choice == "12":
                             print("Delete Student".center(columns))
                             student_manager=Student()
                             email_address = input("Enter student's email address: ")
                             print_records(student_manager.delete_student(email_address))
                        elif choice == "13":
                             print("Display Course".center(columns))
                             course_manager=Course()
                             email_address = get_optional_input("Enter Course ID to display, press enter to skip it: ")
                             print_records(course_manager.display_courses(email_address), ["course_id", "course_name", "description"])
                        elif choice == "14":
                             print("Add new Course".center(columns))
                             course_manager=Course()
                             course_id = input("Enter course id: ")
                             course_name = input("Enter course name: ")
                             description = input("Enter course description: ")
                             print_records(course_manager.add_new_course(course_id,course_name,description))
                        elif choice == "15":
                             print("Delete Course".center(columns))
                             course_manager=Course()
                             course_id = input("Enter course id you want to delete: ")
                             print_records(course_manager.delete_course(course_id))
                        elif choice == "16":
                             print("Display grade report".center(columns))
                             grade_manager=Grades()
                             email_address = input("Enter email address of the student to get grade report, press enter to list all students report: ")
                             records = grade_manager.display_grade_report(email_address)
                             print_records(records, ["Email Address","First_Name","Last_Name","Course_Id","Grade", "Marks"])
                        elif choice == "17":
                             print("Add/Modify Grade for a student".center(columns))
                             grade_manager=Grades()
                             email_address = input("Enter email address of the student to modify report: ")
                             course_id = input("Enter course id: ")
                             marks = input("Enter marks : ")
                             print_records(grade_manager.modify_grade(email_address,course_id,marks))
                        elif choice == "18":
                             print("Delete grade for a student".center(columns))
                             grade_manager=Grades()
                             email_address = input("Enter email address of the student to delete grade: ")
                             course_id = input("Enter course id: ")
                             print_records(grade_manager.delete_grade(email_address,course_id))
                        elif choice == "19":
                             print("Logging out".center(columns))
                             break
                        else:
                            print("Enter Valid choice from the given options")


                elif role == "student":
                    while True:
                        print("=================================".center(columns))
                        print(f"Welcome to the student portal: {email_address}".center(columns))
                        print("=================================".center(columns))
                        print("\n CheckMyGrade Main Menu:")
                        print("1. Display my records")
                        print("2. Check my Grades")
                        print("3. Check my Marks")
                        print("4. Add Student record")
                        print("5. Logout")
                        choice = input("Enter your Choice: ")
                        if choice == "1":
                            print("Details for Student".center(columns))
                            student_manager=Student()
                            records = student_manager.display_record(email_address)
                            print_records(records, ["Email Address","First_Name","Last_Name","Course_Id","Grade", "Marks"])
                        elif choice == "2":
                            print("Check my Grades".center(columns))
                            student_manager=Student()
                            course_id = get_optional_input("Enter course id, press enter to list for all courses: ")
                            records = student_manager.check_my_grades(email_address, course_id)
                            print_records(records, ["Email Address","First_Name","Last_Name","Course_Id","Grade", "Marks"])
                        elif choice == "3":
                            print("Check my Marks".center(columns))
                            student_manager=Student()
                            course_id = get_optional_input("Enter course id, press enter to list for all courses: ")
                            records = student_manager.check_my_marks(email_address, course_id)
                            print_records(records, ["Email Address","First_Name","Last_Name","Course_Id","Grade", "Marks"])
                        elif choice == "4":
                             student_manager=Student()
                             print("Add student".center(columns))
                             first_name = input("Enter student's first name: ")
                             last_name = input("Enter student's last name: ")
                             course_id = input("Enter student's course_id: ")
                             print_records(student_manager.add_new_student(email_address,first_name,last_name,course_id))
                        elif choice == "5":
                             print("Logging out".center(columns))
                             break
                        else:
                            print("Enter Valid choice from the given options")
                else:
                    print(f"User must br student or professor, found {role}")
        elif choice == "2":
            print("Change password".center(columns))
            login_manager = LoginUser()
            email_address = input("Enter Email address: ")
            old_password = getpass.getpass("Enter your old password: ")
            print(login_manager.change_password(email_address, old_password))
        elif choice == "3":
            print("Create signup account!".center(columns))
            login_manager = LoginUser()
            email_address = input("Enter Email address: ")
            password = getpass.getpass("Enter your password: ")
            role = input("Enter Role (student/professor):")
            print(login_manager.create_user(email_address, password, role))
        elif choice == "4":
            break
        else:
            print("Enter valid choice from the given options")


if __name__ == "__main__":
    check_my_grade()
