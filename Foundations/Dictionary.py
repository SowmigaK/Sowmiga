#dictionary
from tkinter import END


student={"name":"sowmiga","age":20,"place":"erode"}
A=dict(name="sowmiga",age=20,place="erode")
print(A)
#values and items
print(student.values())
print(student.items())

#get
print(student.get("name"))
#instead of get we can use [] to access the value
print(student.get("course"))
#print(student["course"]) #this will give error because course is not present in the dictionary

#add
student["course"]="python"
print(student)

#update
student.update({"age":21})
print(student)

#delete
del student["course"]
print(student)

age=student.pop("age")
print(student)
print(age)
#or use the below method to delete the dictionary
d={"a":1,"b":2}
del d
print(d)

#remove the last inserted item
student.popitem()
print(student)

#remove all items from the dictionary

##student={"name":"sowmiga",
         "name":"sowmi"}
#print(student)

for value in student.values():
    print(value,END="")

 #copy
 # fromkeys
keys=["name","age","place"]
d= dict.fromkeys(keys,"not available")
print(d)

 # setdefault
course=student.setdefault("course","python")
print(course)

#nested dictionary
student={student1:{"name":"sowmiga","age":20,},student2:{"name":"sowmi","age":29,}}
print(student(student1(age)))

#int
#float as a key
#tuple as a key
#but we cannot use set or list as a key because they are mutable
#we use float,tuple,list,set as a value in the dictionary


