# coding =utf8
import os

rows = []
path = "data_cssci"
for files in os.walk(path):
    for filename in files[2]:
        print(filename)
        with open(path + "\\" + filename, 'r', encoding="utf8") as file:
            lines = file.readlines()

            for line in lines:
                rows.append(line)

with open( 'cssci.txt', 'a', encoding="utf8") as file1:
    print(len(rows))
    for rs in rows:
        file1.write(rs )