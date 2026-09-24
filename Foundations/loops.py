#for loop

#1)printing numbers from 0 to 5
for i in range(6):
    print(i)

#2)printing numbers from 1 to 5
for i in range(1, 6):
    print(i)

#3)print even numbers and odd numbers
for i in range(2, 11, 2):
    print(i)

for i in range(1,11,2):
    print(i)

#4)print 10 to 1 in descending order
for i in range(11, 0, -1):
    print(i)

#5)print numbers from 1 to 10 and their squares
for i in range(1,11):
    i=i**2
    print(i)

#6)add all numbers from 1 to 10 (eg. 1+2+3+4+5+6+7+8+9+10)
total=0
for i in range(1,11):
    total=total+i
print(total)



