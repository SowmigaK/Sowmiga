#program to find grade of student based on marks
mark=int(input("Enter mark:"))
if mark>=50 and mark<75:
    print("Grade C")
elif mark>=75 and mark<90:
    print("Grade B")
elif mark>=90 and mark<=100:
    print("Grade A")
else:
    print("Fail")

#KEY POINTS:(else is not mandatory in if else and if elif statements)
#we can use elif for n number times in if elif else statements

#elif ladder(more than 1 elif statement in a program)
#Program to find grade of student based on marks
mark=int(input("Enter mark:"))
if mark>=50 and mark<75:
    print("Pass")
elif mark>=75 and mark<90:
    print("Good")
elif mark>=90 and mark<=100:
    print("Excellent")
else:
    print("Fail")

#nested if else
mark=int(input("Enter mark:"))
if mark>=50:
    if mark>=65:
        print("First class")
    else:
        print("Pass")
else:
    print("Fail")        

#program to find age group of person
age=int(input("Enter age:"))
if age>=18:
    if age>=21:
        if age>=60:
            print("Age is 25 or above")
        else:
            print("age is between 21 and 24")
    else:
        print("age is between 18 and 21")
else:
    print("Below 18")

#match choice statement
choice=int(input("Enter choice:"))
match choice:
    case 1:
        print("Pizza selected")
    case 2:
        print("Burger selected")
    case 3:
        print("pasta selected")
    case 4:
        print("Biriyani selected")
    case _:
        print("Invalid choice")
        

