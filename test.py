import os
thisPath = os.getcwd()
path = thisPath.replace("\\", "\\\\") + "\\\\RootCiteProject" + "\\\\data_wos"
print(path)

for files in os.walk(path):
    for filename in files[2]:
        print(filename)
