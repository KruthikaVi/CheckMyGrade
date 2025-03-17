import unittest
from unittest.mock import patch
from check_my_grade import Student, Grades, LoginUser, Professor, Course
from encdyc import TextSecurity


class TestCheckMyGrade(unittest.TestCase):
    def setUp(self):
        # Initializing test objects and dummy data
        self.student_manager = Student()
        self.login_manager = LoginUser()
        self.professor_manager = Professor()
        self.course_manager = Course()
        self.grades_manager = Grades()
        self.dummy_user = ["test@gmail.com", "test123", "student"]
        self.dummy_user2 = ["john@gmail.com", "test123", "professor"]
        self.dummy_student = ["test@gmail.com", "John", "AAAA", "TEST101", "77"]
        self.dummy_course = ["TEST101", "Python", "Python description"]
        self.dummy_professor = [
            "john@gmail.com",
            "Peter White",
            "Associate Professor",
            "TEST101",
        ]
        self.cipher = TextSecurity(4)

        # Create user and student before running tests
        self.course_manager.add_new_course(*self.dummy_course)
        self.login_manager.create_user(*self.dummy_user)
        self.login_manager.create_user(*self.dummy_user2)
        self.student_manager.add_new_student(*self.dummy_student)
        self.professor_manager.add_new_professor(*self.dummy_professor)

    def tearDown(self):
        # Clean up after each test
        self.course_manager.delete_course(self.dummy_course[0])
        self.student_manager.delete_student(self.dummy_user[0])
        self.professor_manager.delete_professor(self.dummy_user2[0])
        self.login_manager.delete_record(self.dummy_user[0])
        self.login_manager.delete_record(self.dummy_user2[0])

    def test_students_length(self):
        """Test if the number of students is >= 1000."""
        self.assertGreaterEqual(
            len(self.student_manager.students),
            1000,
            "Too few students, at least 1000 student records are required",
        )

    def test_encrypt_decrypt(self):
        """Test encryption and decryption functionality."""
        test_string = "test123"
        encrypted = self.cipher.encrypt(test_string)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(decrypted, test_string, "Encryption and Decryption mismatch")

    @patch("getpass.getpass", return_value="test129")
    def test_login_user(self, mock_getpass):
        """Test user login and password update."""
        login = self.login_manager.login(self.dummy_user[0], self.dummy_user[1])
        self.assertTrue(login[0])

        # Change the password and verify login again
        self.login_manager.change_password(self.dummy_user[0], self.dummy_user[1])
        login = self.login_manager.login(self.dummy_user[0], "test129")
        self.assertTrue(login[0])

    def test_check_student_grades(self):
        """Test checking grades for a student."""
        check_grade = self.student_manager.check_my_grades(self.dummy_student[0])
        self.assertEqual(
            check_grade, [["test@gmail.com", "John", "AAAA", "TEST101", "77", "C"]]
        )

    def test_update_student_record(self):
        """Test updating student record."""
        # Update record and check for updated marks
        self.student_manager.update_student_record(
            self.dummy_student[0], self.dummy_student[3], 90
        )
        check_marks = self.student_manager.check_my_marks(self.dummy_student[0])
        self.assertEqual(
            check_marks, [["test@gmail.com", "John", "AAAA", "TEST101", "90", "A"]]
        )

    def test_sort_students(self):
        """Test sorting students by last name."""
        records = self.student_manager.sort_students(2)
        self.assertEqual(
            records[0], ["test@gmail.com", "John", "AAAA", "TEST101", "77", "C"]
        )

    def test_display_student_records(self):
        """Test displaying student records."""
        records = self.student_manager.display_record(self.dummy_student[0])
        self.assertEqual(
            records, [["test@gmail.com", "John", "AAAA", "TEST101", "77", "C"]]
        )

    def test_add_and_delete_student(self):
        """Test adding and deleting a student."""
        self.student_manager.delete_student(self.dummy_user[0])
        add_new_student = self.student_manager.add_new_student(*self.dummy_student)
        self.assertEqual(
            add_new_student,
            f"Successfully added student info for {self.dummy_student[0]}",
        )

    def test_add_professor(self):
        """Test adding and deleting a professor."""
        self.professor_manager.delete_professor(self.dummy_professor[0])
        add_new_professor = self.professor_manager.add_new_professor(
            *self.dummy_professor
        )
        self.assertEqual(
            add_new_professor,
            f"Successfully added professor info for {self.dummy_professor[0]}",
        )

    def test_display_professor_details(self):
        """Test displaying professor records."""
        records = self.professor_manager.professor_course_details(
            self.dummy_professor[0]
        )
        self.assertEqual(records, [self.dummy_professor])

    def test_modify_professor(self):
        """Test updating professor record."""
        # Update record and check for updated record
        self.professor_manager.modify_professor_details(self.dummy_professor[0], "Sam")
        display_professor = self.professor_manager.professor_course_details(
            self.dummy_professor[0]
        )
        self.assertEqual(
            display_professor,
            [["john@gmail.com", "Sam", "Associate Professor", "TEST101"]],
        )

    def test_add_course(self):
        """Test adding and deleting a course."""
        self.course_manager.delete_course(self.dummy_course[0])
        add_new_course = self.course_manager.add_new_course(*self.dummy_course)
        self.assertEqual(
            add_new_course, f"Course {self.dummy_course[0]} added successfully!"
        )

    def test_display_course_details(self):
        """Test displaying course details."""
        records = self.course_manager.display_courses(self.dummy_course[0])
        self.assertEqual(records, [self.dummy_course])


if __name__ == "__main__":
    unittest.main()
