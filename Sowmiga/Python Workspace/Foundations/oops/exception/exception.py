# age=int(input("enter age"))
# print(age)
# file=open('CSV_handling.py','r')
# print(file.read())
# file=open(r'C:\Users\ELCOT\Desktop\Sowmiga\Python Workspace\oops\file_handling\CSV_handling.py','r')
# print(file.read())

#try and except
#when use try if it is sucess it goes else part,if it is fail go to except part.
# try:
#     a=int(input("enter age"))
# except:
#     print("enter valid number")
# else:
#     print("valid number",a)

# #Raise
# n=int(input("enter number"))
# if 0<= n <=100:
#     print(n)
# #python doesnot shows the error here .but according to us it is an error/we want to show this is an error in this case we use raise
# raise("number is not in the range")
# #now it shows error.

try:
    user_name=input("enter user name")
except:
    print("Enter valid user_name")
else:
    print("user_name",user_name)
