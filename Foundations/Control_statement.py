#Control staements
#Break,continue,Pass 
#KEY POINTS : bREAK-Stop completely(loop stops)
#Continue-Skip this turn(next)
#Pass-Do nothing (placeholder)

#Break
for i in range (1,6):
    if i==3:
        break
    print(i)

#Continue
for i in range(1,6):
    if i==3:
        continue
    print(i)

#pass
for i in range(1,6):
    if i==3:
        pass
    print(i)

#printing name and percentage of 5 students using for loop
for i in range(5):
    name=input("Enter name:")
    percentage=int(input("Enter percentage:"))
    print(name, "-", percentage)

# %<50-don't print,%=100 -stop the program, %50-100 -print name and percentage
for i in range(5):
    name = input("Enter name: ")
    percentage = int(input("Enter percentage: "))
    if percentage == 100:
        break
    if percentage >= 50: 
        print(name, "-", percentage)