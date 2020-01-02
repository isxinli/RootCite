import os
from datasketch import MinHashLSH, MinHash

def deduplication(path, resultPath):
    ArticleLines = []
    with open(path, 'r', encoding='utf8') as readFile:
        print("-----------------开始对" + path + "文件进行去重---------------------------")
        readFile.readline()
        lines = readFile.readlines()
        for article in lines:
            ArticleLines.append(article)

        lsh = MinHashLSH(threshold=0.98, num_perm=128)
        for line in ArticleLines:
            x = '\t'.join(line.split('\t')[:-1])
            m = MinHash(num_perm=128)
            for d in x:
                # 哈希化
                m.update(d.encode('utf8'))
            lsh.insert(line, m)

    print('------------------------哈希化完成----------------------------')

    NEW = []
    print("-----------------在对数据进行相似度计算、合并、去重，花费时间较多，请耐心等待-----------------------" + "\n")
    while len(ArticleLines) > 0:
        x = '\t'.join(ArticleLines[0].split('\t')[:-1])
        value = 0
        m1 = MinHash(num_perm=128)
        for d in x:
            # 哈希化
            m1.update(d.encode('utf8'))
        result = lsh.query(m1)

        if len(result) > 1:
            for rs in result:
                # 对参考文献的数量进行加和
                value = value + int(rs.split("\t")[2].replace('\n', ''))
                # 并删除这些元素
                if rs in ArticleLines:
                    ArticleLines.remove(rs)
            NEW.append('\t'.join([x, str(value)]) + '\n')
        else:
            NEW.append(ArticleLines[0])
            del ArticleLines[0]

    with open(resultPath, 'a', encoding='utf8', newline='') as resultFile:
        resultFile.write("year\tCR\tcited times\n")
        for row in NEW:
            resultFile.write(row)


if os.path.isfile("year_cssci.csv"):
    deduplication("year_cssci.csv", "result_cssci.csv")
    os.remove('year_cssci.csv')
else:
    print("请先使用rpys.exe和year.exe生成初始结果")
if os.path.isfile("year_wos.csv"):
    deduplication("year_wos.csv", "result_wos.csv")
    os.remove('year_wos.csv')
else:
    print("请先使用rpys.exe和year.exe生成初始结果")

print('-------------------处理完成，请在根目录下查收result_CSSCI.csv、result_WOS.csv文件进行分析-------------------------')

