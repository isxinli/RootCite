# coding = utf8
import re
import os
'''
将在web of science下载的多个题录文件放到data文件夹下
将多个文件整合成一个文件
并命名为wos.txt
'''
rows = []
path = "data_wos"
for files in os.walk(path):
    for filename in files[2]:
        print(filename)
        with open(path + "\\" + filename, 'r', encoding='utf8') as file:
            # 文件的字段名
            fieldname= re.split('[\t\n]', file.readline())[:-1]
            # 文件字段名
            # print(fieldname)
            # 字段数目68
            # print(len(fieldname))

            lines = file.readlines()
            for line in lines:
                row = re.split('[\t]', line)[:-1]
                rows.append(row)

with open( 'wos.txt', 'a', encoding='utf8', newline='') as file1:
    print(len(rows))
    for rs in rows:
        rs = '\t'.join(rs)
        # print(rs)
        file1.write(rs + '\n')






