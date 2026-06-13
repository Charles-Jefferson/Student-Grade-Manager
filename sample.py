"""
Student Registration System
A simple console-based application to manage student registrations
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Student:
    """Student class to store individual student information hello4"""
    
    def __init__(self, student_id: str, name: str, age: int, email: str, course: str):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.email = email
        self.course = course
        self.registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """Convert student object to dictionary for JSON storage"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'course': self.course,
            'registration_date': self.registration_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        """Create student object from dictionary asdad hello1"""
        student = cls(
            data['student_id'],
            data['name'],
            data['age'],
            data['email'],
            data['course']
        )
        student.registration_date = data.get('registration_date', 'Unknown')
        return student
    
    def __str__(self) -> str:
        return f"ID: {self.student_id} | Name: {self.name} | Course: {self.course}"


class RegistrationSystem:
    """Main registration system to manage students"""
    
    def __init__(self, data_file: str = "students.json"):
        self.data_file = data_file
        self.students: Dict[str, Student] = {}
        self.load_data()
    
    def load_data(self):
        """Load student data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    for student_data in data:
                        student = Student.from_dict(student_data)
                        self.students[student.student_id] = student
                print(f"Loaded {len(self.students)} existing students.")
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def save_data(self):
        """Save student data to JSON file"""
        try:
            data = [student.to_dict() for student in self.students.values()]
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def register_student(self):
        """Register a new student"""
        print("\n" + "="*50)
        print("NEW STUDENT REGISTRATION")
        print("="*50)
        
        # Get student ID
        while True:
            student_id = input("Enter Student ID (e.g., S001): ").strip()
            if not student_id:
                print("Student ID cannot be empty!")
            elif student_id in self.students:
                print(f"Student with ID {student_id} already exists!")
            else:
                break
        
        # Get name
        while True:
            name = input("Enter Full Name: ").strip()
            if name and all(c.isalpha() or c.isspace() for c in name):
                break
            print("Please enter a valid name (letters and spaces only)!")
        
        # Get age
        while True:
            try:
                age = int(input("Enter Age: "))
                if 5 <= age <= 120:
                    break
                print("Please enter a valid age between 5 and 120!")
            except ValueError:
                print("Please enter a valid number!")
        
        # Get email
        while True:
            email = input("Enter Email: ").strip()
            if '@' in email and '.' in email:
                break
            print("Please enter a valid email address!")
        
        # Get course
        courses = ["Computer Science", "Business Administration", "Engineering", 
                   "Mathematics", "Physics", "English Literature"]
        print("\nAvailable Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course}")
        
        while True:
            try:
                choice = int(input("Select course (1-6): "))
                if 1 <= choice <= len(courses):
                    course = courses[choice - 1]
                    break
                print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
        
        # Create and register student
        student = Student(student_id, name, age, email, course)
        self.students[student_id] = student
        self.save_data()
        
        print("\n" + "✓"*30)
        print("STUDENT REGISTERED SUCCESSFULLY!")
        print(f"Registration Date: {student.registration_date}")
        print("✓"*30)
    
    def view_all_students(self):
        """Display all registered students"""
        if not self.students:
            print("\nNo students registered yet.")
            return
        
        print("\n" + "="*80)
        print("ALL REGISTERED STUDENTS")
        print("="*80)
        print(f"{'ID':<10} {'Name':<25} {'Age':<5} {'Course':<25}")
        print("-"*80)
        
        for student in self.students.values():
            print(f"{student.student_id:<10} {student.name[:24]:<25} "
                  f"{student.age:<5} {student.course[:24]:<25}")
        print("="*80)
        print(f"Total Students: {len(self.students)}")
    
    def search_student(self):
        """Search for a student by ID or name"""
        if not self.students:
            print("\nNo students registered yet.")
            return
        
        print("\n" + "="*50)
        print("SEARCH STUDENT")
        print("="*50)
        search_term = input("Enter Student ID or Name: ").strip().lower()
        
        found_students = []
        for student in self.students.values():
            if (search_term in student.student_id.lower() or 
                search_term in student.name.lower()):
                found_students.append(student)
        
        if found_students:
            print(f"\nFound {len(found_students)} student(s):")
            print("-"*80)
            for student in found_students:
                print(f"\nStudent ID: {student.student_id}")
                print(f"Name: {student.name}")
                print(f"Age: {student.age}")
                print(f"Email: {student.email}")
                print(f"Course: {student.course}")
                print(f"Registered: {student.registration_date}")
                print("-"*40)
        else:
            print("\nNo students found matching your search.")
    
    def update_student(self):
        """Update student information"""
        if not self.students:
            print("\nNo students registered yet.")
            return
        
        print("\n" + "="*50)
        print("UPDATE STUDENT INFORMATION")
        print("="*50)
        
        student_id = input("Enter Student ID to update: ").strip()
        
        if student_id not in self.students:
            print("Student not found!")
            return
        
        student = self.students[student_id]
        print(f"\nCurrent Information for {student.name}:")
        print(f"1. Name: {student.name}")
        print(f"2. Age: {student.age}")
        print(f"3. Email: {student.email}")
        print(f"4. Course: {student.course}")
        print("5. Cancel")
        
        choice = input("\nWhat would you like to update? (1-5): ").strip()
        
        if choice == '1':
            new_name = input("Enter new name: ").strip()
            if new_name:
                student.name = new_name
                print("Name updated successfully!")
        elif choice == '2':
            try:
                new_age = int(input("Enter new age: "))
                if 5 <= new_age <= 120:
                    student.age = new_age
                    print("Age updated successfully!")
                else:
                    print("Invalid age!")
            except ValueError:
                print("Invalid input!")
        elif choice == '3':
            new_email = input("Enter new email: ").strip()
            if '@' in new_email and '.' in new_email:
                student.email = new_email
                print("Email updated successfully!")
            else:
                print("Invalid email!")
        elif choice == '4':
            new_course = input("Enter new course: ").strip()
            if new_course:
                student.course = new_course
                print("Course updated successfully!")
        elif choice == '5':
            print("Update cancelled.")
        else:
            print("Invalid choice!")
        
        if choice in ['1', '2', '3', '4']:
            self.save_data()
    
    def delete_student(self):
        """Delete a student from the system"""
        if not self.students:
            print("\nNo students registered yet.")
            return
        
        print("\n" + "="*50)
        print("DELETE STUDENT")
        print("="*50)
        
        student_id = input("Enter Student ID to delete: ").strip()
        
        if student_id not in self.students:
            print("Student not found!")
            return
        
        student = self.students[student_id]
        print(f"\nStudent to delete: {student.name} ({student.student_id})")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            del self.students[student_id]
            self.save_data()
            print("Student deleted successfully!")
        else:
            print("Deletion cancelled.")
    
    def show_statistics(self):
        """Display registration statistics"""
        if not self.students:
            print("\nNo students registered yet.")
            return
        
        print("\n" + "="*50)
        print("REGISTRATION STATISTICS")
        print("="*50)
        
        # Course distribution
        course_count = {}
        for student in self.students.values():
            course_count[student.course] = course_count.get(student.course, 0) + 1
        
        print("\nCourse Distribution:")
        for course, count in sorted(course_count.items()):
            print(f"  {course}: {count} student(s)")
        
        # Age statistics
        ages = [student.age for student in self.students.values()]
        print(f"\nAge Statistics:")
        print(f"  Average Age: {sum(ages)/len(ages):.1f}")
        print(f"  Youngest: {min(ages)}")
        print(f"  Oldest: {max(ages)}")
        
        print(f"\nTotal Registered Students: {len(self.students)}")
    
    def main_menu(self):
        """Display the main menu and handle user input"""
        while True:
            print("\n" + "="*50)
            print("STUDENT REGISTRATION SYSTEM")
            print("="*50)
            print("1. Register New Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student Information")
            print("5. Delete Student")
            print("6. View Statistics")
            print("7. Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.register_student()
            elif choice == '2':
                self.view_all_students()
            elif choice == '3':
                self.search_student()
            elif choice == '4':
                self.update_student()
            elif choice == '5':
                self.delete_student()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                print("\nThank you for using the Student Registration System!")
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please enter 1-7.")


def main():
    """Main function to run the registration system"""
    system = RegistrationSystem()
    system.main_menu()


if __name__ == "__main__":
    main()