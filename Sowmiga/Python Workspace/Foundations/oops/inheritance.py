class person:
    def_init_(self,name,email,dept):
        self.name=Name
        self.email=email
    def display_role(self):
        return "University person"
class student(person):
    def_init_(self,name,email,dept):
        super()._init_(name,email)
        self.dept=deptt
        return "student"
class Teacher(student):
    def_init_(self,name,email,dept,subjects_handled):
    super()._init_(name,email,dept,subjects_handling)
    self.subjects_handling=subjects_handling
    return "Teacher"
std1=student("ABC","abc@gmail.com","")
print(std1.display_role())

class Animal:
    def sound(self):
        return"any sound"

class dog:
    def sound(self):
        return"bark"

class bird:
    def sound(self):
        return"sing"
bird1=bird()
print(bird1)

people=[
    student("raj",raj@gmail.com,AI)
    Teacher("cheran",cheran@gmail.com,CSE,[AI,cs])
]
for person in people:
    print(person.display())