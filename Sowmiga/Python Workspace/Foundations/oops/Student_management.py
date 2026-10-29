class Student:
    def __init__(self, id, name, department, marks, attendance):
        self.id = id
        self.name = name
        self.department = department
        self.marks = marks
        #self._ that _is used for encapsulation(limit and product(we cannot able to see it outside))
        #limits-setter and product-getter
        self._attendance = attendance

    def display(self):
        return f"Name: {self.name}"

    def avg(selfreturn round(sum.self)):

std1 = Student(101, "Sowmi", "Mathematics", [85, 90])
std2 = Student(102, "Vinothini", "Computer Science", [78, 85])
std3 = Student(103, "Priya", "Physics", [92, 95])
std4 = Student(104, "Divya", "Chemistry", [74, 80])
std5 = Student(105, "Anitha", "Mathematics", [88, 91])

print(std1.display())
