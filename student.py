"""
Sample Python Program: Student Grade Manager
This program demonstrates:
- Classes and objects
- File handling
- Exception handling
- List comprehensions
- Dictionary operations
- User input processing
"""

import json
import os
from datetime import datetime

class Student:
    """Represents a student with their grades asd sadad hello3"""
    
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.grades = {}
    
    def add_grade(self, subject, grade):
        """Add or update a grade for a subject"""
        if 0 <= grade <= 100:
            self.grades[subject] = grade
            return True
        return False
    
    def get_average(self):
        """Calculate average grade"""
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)
    
    def get_letter_grade(self):
        """Convert numerical grade to letter grade"""
        avg = self.get_average()
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'
    
    def to_dict(self):
        """Convert student data to dictionary"""
        return {
            'name': self.name,
            'student_id': self.student_id,
            'grades': self.grades,
            'average': self.get_average(),
            'letter_grade': self.get_letter_grade()
        }
    
    def __str__(self):
        return f"Student: {self.name} (ID: {self.student_id}) | Average: {self.get_average():.1f} | Grade: {self.get_letter_grade()}"


class GradeManager:
    """Manages multiple students and their grades"""
    
    def __init__(self, filename='students_data.json'):
        self.students = {}
        self.filename = filename
        self.load_data()
    
    def add_student(self, name, student_id):
        """Add a new student"""
        if student_id in self.students:
            print(f"Student with ID {student_id} already exists!")
            return False
        
        self.students[student_id] = Student(name, student_id)
        print(f"Student {name} added successfully!")
        return True
    
    def add_grade(self, student_id, subject, grade):
        """Add a grade for a student"""
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found!")
            return False
        
        if self.students[student_id].add_grade(subject, grade):
            print(f"Grade {grade} added for {subject}")
            return True
        else:
            print("Invalid grade! Grade must be between 0 and 100.")
            return False
    
    def display_student_info(self, student_id):
        """Display information for a specific student"""
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found!")
            return
        
        student = self.students[student_id]
        print("\n" + "="*50)
        print(f"Student Information")
        print("="*50)
        print(f"Name: {student.name}")
        print(f"ID: {student.student_id}")
        print(f"Average: {student.get_average():.2f}")
        print(f"Letter Grade: {student.get_letter_grade()}")
        print("\nGrades:")
        if student.grades:
            for subject, grade in student.grades.items():
                print(f"  {subject}: {grade}")
        else:
            print("  No grades recorded yet")
        print("="*50)
    
    def display_all_students(self):
        """Display all students"""
        if not self.students:
            print("No students in the system.")
            return
        
        print("\n" + "="*60)
        print(f"All Students (Total: {len(self.students)})")
        print("="*60)
        for student in self.students.values():
            print(student)
        print("="*60)
    
    def get_top_performers(self, count=3):
        """Get top performing students"""
        if not self.students:
            return []
        
        sorted_students = sorted(
            self.students.values(), 
            key=lambda s: s.get_average(), 
            reverse=True
        )
        return sorted_students[:count]
    
    def save_data(self):
        """Save student data to JSON file"""
        try:
            data = {
                student_id: student.to_dict() 
                for student_id, student in self.students.items()
            }
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Data saved to {self.filename}")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self):
        """Load student data from JSON file"""
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            for student_id, student_data in data.items():
                student = Student(student_data['name'], student_id)
                student.grades = student_data['grades']
                self.students[student_id] = student
            
            print(f"Loaded {len(self.students)} students from {self.filename}")
        except Exception as e:
            print(f"Error loading data: {e}")


def main():
    """Main program loop"""
    manager = GradeManager()
    
    while True:
        print("\n" + "="*40)
        print(" STUDENT GRADE MANAGER")
        print("="*40)
        print("1. Add new student")
        print("2. Add grade for student")
        print("3. View student information")
        print("4. View all students")
        print("5. View top performers")
        print("6. Save data")
        print("7. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            name = input("Enter student name: ").strip()
            student_id = input("Enter student ID: ").strip()
            manager.add_student(name, student_id)
        
        elif choice == '2':
            student_id = input("Enter student ID: ").strip()
            subject = input("Enter subject: ").strip()
            try:
                grade = float(input("Enter grade (0-100): "))
                manager.add_grade(student_id, subject, grade)
            except ValueError:
                print("Invalid grade! Please enter a number.")
        
        elif choice == '3':
            student_id = input("Enter student ID: ").strip()
            manager.display_student_info(student_id)
        
        elif choice == '4':
            manager.display_all_students()
        
        elif choice == '5':
            top_students = manager.get_top_performers()
            if top_students:
                print("\n🏆 TOP PERFORMERS 🏆")
                for i, student in enumerate(top_students, 1):
                    print(f"{i}. {student.name} - Average: {student.get_average():.2f}")
            else:
                print("No students in the system.")
        
        elif choice == '6':
            manager.save_data()
        
        elif choice == '7':
            save_choice = input("Save data before exiting? (y/n): ").lower()
            if save_choice == 'y':
                manager.save_data()
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    # Demonstrate list comprehension and some other features
    sample_grades = [85, 92, 78, 90, 88]
    print("Sample Grade Analysis:")
    print(f"Original grades: {sample_grades}")
    print(f"Grades above 85: {[g for g in sample_grades if g > 85]}")
    print(f"Rounded average: {sum(sample_grades)/len(sample_grades):.0f}")
    print("\n" + "="*40)
    
    # Run the main program
    main()