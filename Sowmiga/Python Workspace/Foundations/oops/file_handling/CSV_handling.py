import csv
with open(r"c:\Users\Anudip\Desktop\Python_B3\File_handling\data.csv","r") as file:
    reader=csv.reader(file)
    #for row in file:
    #   print(row)
    #print(file)
    reader=csv.dictreader(file)
    for row in reader:
        print(row["name"])