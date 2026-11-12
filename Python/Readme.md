# Nova University – Student Management System

## 1. Business Problem

Nova University requires a simple application to maintain student and faculty information and perform basic academic checks. Managing student details, attendance, marks, and faculty information requires a structured approach to ensure accurate academic records and efficient information management.

## 2. Business Objective

To develop a Python-based Student Management System using Object-Oriented Programming (OOP) concepts. The application maintains multiple student and faculty records, checks attendance eligibility, calculates academic results, and handles invalid inputs.

## 3. Business Requirements

- How can student information be maintained?
- How can faculty information be managed?
- How can students' attendance eligibility be checked?
- How can total marks and average marks be calculated?
- How can student results and grades be determined?
- How can invalid attendance and marks inputs be handled?
- How can multiple student and faculty records be maintained?

## 4. Application Details

| Component | Description |
| ------------------ | ------------------------------------------------ |
| Application Name | Nova University Student Management System |
| Application Type | Python-Based Console Application |
| Main Entities | Person, Student, Faculty, University |
| Programming Language | Python |
| Interface | Console-Based |
| Data Storage | In-Memory Lists |

## 5. Tools and Technologies Used

- Python
- Object-Oriented Programming (OOP)
- VS Code
- Python Classes and Objects
- Python Lists
- Conditional Statements
- Exception Handling

## 6. Application Design and Implementation

- Created a `Person` class to maintain common information such as name, email, and phone number.
- Implemented a `Student` class inheriting from the `Person` class.
- Implemented a `Faculty` class inheriting from the `Person` class.
- Created a `University` class to manage multiple student and faculty records.
- Implemented academic calculations for total marks, average marks, results, and grades.
- Added attendance validation and examination eligibility checks.
- Used exception handling to manage invalid numeric inputs.
- Implemented a menu-driven console application for user interaction.

## 7. Academic Rules and Calculations

| Academic Rule | Condition |
| ------------------ | ------------------------------------------------ |
| Attendance Eligibility | Attendance of 75% or above |
| Pass Criteria | Average marks of 50 or above |
| Total Marks | Sum of Python, SQL, and Excel marks |
| Average Marks | Total marks divided by 3 |
| Grade A+ | Average marks of 90 or above |
| Grade A | Average marks of 80 or above |
| Grade B | Average marks of 70 or above |
| Grade C | Average marks of 60 or above |
| Grade D | Average marks of 50 or above |
| Grade F | Average marks below 50 |

## 8. Application Features

The console application includes the following functionalities:

**Student Management**

- Add Student
- View Students
- Check Attendance Eligibility
- View Academic Results

**Faculty Management**

- Add Faculty
- View Faculty

**Academic Calculations**

- Total Marks Calculation
- Average Marks Calculation
- Pass/Fail Result
- Grade Calculation
- Attendance Eligibility Check

**Input Validation**

- Attendance validation between 0 and 100.
- Marks validation between 0 and 100.
- Handling non-numeric inputs.
- Duplicate Student ID and Faculty ID checks.
- Invalid menu choice handling.

## 9. OOP Concepts Used

- **Classes and Objects:** Used to represent students, faculty members, and university management.
- **Inheritance:** Student and Faculty classes inherit common attributes from the Person class.
- **Encapsulation:** Student and faculty information and their related methods are organized within their respective classes.
- **Abstraction:** Application operations are organized into methods to simplify interaction and implementation.
- **Code Reusability:** Common person information and academic calculation methods are reused where applicable.

## 10. Validation and Testing

The application is designed to handle valid and invalid inputs based on the business requirements.

| Test Area | Test Input | Expected Behaviour |
| ------------------ | ------------------ | ------------------------------------------------ |
| Attendance | 75 | Valid and eligible |
| Attendance | 0 | Valid value |
| Attendance | 100 | Valid value |
| Attendance | -5 | Invalid input |
| Attendance | 105 | Invalid input |
| Academic Marks | Valid numeric values | Calculate total, average, result, and grade |
| User Input | Non-numeric values | Display an error message |
| Student Records | Duplicate Student ID | Prevent duplicate entry |
| Faculty Records | Duplicate Faculty ID | Prevent duplicate entry |

## 11. Project Outcome

Developed a Python-based Student Management System using Object-Oriented Programming concepts. The application provides structured student and faculty management, academic calculations, attendance eligibility checks, and input validation through a menu-driven console interface.