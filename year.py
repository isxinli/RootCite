import re
import os


'''
读取题录数据
得到每一篇文献的详细元数据信息
以year.csv格式存储
'''
# 设定起止年份范围
Year = ['1700', '1701', '1702', '1703', '1704', '1705', '1706', '1707', '1708', '1709', '1710', '1711', '1712', '1713',
            '1714', '1715', '1716', '1717', '1718', '1719', '1720', '1721', '1722', '1723', '1724', '1725', '1726', '1727',
            '1728', '1729', '1730', '1731', '1732', '1733', '1734', '1735', '1736', '1737', '1738', '1739', '1740', '1741',
            '1742', '1743', '1744', '1745', '1746', '1747', '1748', '1749', '1750', '1751', '1752', '1753', '1754', '1755',
            '1756', '1757', '1758', '1759', '1760', '1761', '1762', '1763', '1764', '1765', '1766', '1767', '1768', '1769',
            '1770', '1771', '1772', '1773', '1774', '1775', '1776', '1777', '1778', '1779', '1780', '1781', '1782', '1783',
            '1784', '1785', '1786', '1787', '1788', '1789', '1790', '1791', '1792', '1793', '1794', '1795', '1796', '1797',
            '1798', '1799', '1800', '1801', '1802', '1803', '1804', '1805', '1806', '1807', '1808', '1809', '1810', '1811',
            '1812', '1813', '1814', '1815', '1816', '1817', '1818', '1819', '1820', '1821', '1822', '1823', '1824', '1825',
            '1826', '1827', '1828', '1829', '1830', '1831', '1832', '1833', '1834', '1835', '1836', '1837', '1838', '1839',
            '1840', '1841', '1842', '1843', '1844', '1845', '1846', '1847', '1848', '1849', '1850', '1851', '1852', '1853',
            '1854', '1855', '1856', '1857', '1858', '1859', '1860', '1861', '1862', '1863', '1864', '1865', '1866', '1867',
            '1868', '1869', '1870', '1871', '1872', '1873', '1874', '1875', '1876', '1877', '1878', '1879', '1880', '1881',
            '1882', '1883', '1884', '1885', '1886', '1887', '1888', '1889', '1890', '1891', '1892', '1893', '1894', '1895',
            '1896', '1897', '1898', '1899', '1900', '1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908', '1909',
            '1910', '1911', '1912', '1913', '1914', '1915', '1916', '1917', '1918', '1919', '1920', '1921', '1922', '1923',
            '1924', '1925', '1926', '1927', '1928', '1929', '1930', '1931', '1932', '1933', '1934', '1935', '1936', '1937',
            '1938', '1939', '1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', '1950', '1951',
            '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963', '1964', '1965',
            '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979',
            '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993',
            '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
            '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

'''
# 将data.txt文件中每篇文献的参考文献数据一条一条读入列表data
# 如果一篇文献以数字开头就是参考文献
# 返回data列表，即该文件中的所有参考文献
'''
# def deSame(TEXT):
#     x = TEXT[0].replace(',,', ',')
#     value = int(x.split('\t')[2])
#     del TEXT[0]
#
#     for y in TEXT:
#         if "no journal" in y:
#             pass
#         elif Levenshtein.ratio(x,y) > 0.95:
#             value = int(value) + int(y.split("\t")[2])
#             TEXT.remove(y)
#     z = x.split('\t')
#     newElement ="\t".join([z[0], z[1], str(value)])
#     return(newElement)

def readDataTxt(dataPath):
    data = []
    with open(dataPath, encoding="utf8") as dataFile:
        while 1:
            line = dataFile.readline()
            if not line:
                break
            if line.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
                data.append(line.replace("\n", ""))
    return data

'''
# 将参考文献处理好
# 格式是“作者+标题+期刊+年份”
# 全部放到一个列表Articles
'''

def getArticles(data):
    Articles = []
    for d in data:
        d = d.replace('..', '.').replace(',,', ',').replace('，，', '，')
        if len(re.findall('[A-Z][.][A-Z][.]', d)) > 0:
            authorRe = re.findall('[A-Z][.][A-Z][.]', d)[0]
            authorSignal = authorRe.replace('.', '')
            d = d.replace(authorRe, authorSignal + '.')
        article = d.split(".")
        # 每篇文献的作者
        author = article[1].lower()
        # 每篇文献的标题
        if len(article) > 3:
            title = article[2].lower()
        else:
            title = "NA"

        # 每篇文献的期刊或出版社
        yearList = re.split(r'[:,]', article[-1])
        if '学位论文' in d:
            if len(d.split('.')) > 3:
                journal = d.split('.')[3].split('，')[0]
        elif '出版社，' in d:
            if len(d.split('.')) > 3:
                journal = d.split('.')[3].replace(',', '，').split('，')[0]
            else:
                journal = d
        elif len(article) > 4:
            if article[3]:
                journal = article[3].lower()
            else:
                journal = "NA"
        elif len(yearList) > 3:
            journal = yearList[-3]
        else:
            journal = "NA"
        # 每篇文献的发表年份
        if '学位论文' in d:
            year = d.split(',')[-1]
            if year in Year:
                year = year
            else:
                year = 'NA'
        elif '出版社，' in d:
            year = d.split('出版社，')[1].replace(":", "")
            if year in Year:
                year = year
            else:
                year = 'NA'
        elif article[-1].split(":")[0] in Year:
            year = article[-1].split(":")[0]
        elif article[-2].split(":")[0] in Year:
            year = article[-2].split(":")[0]
        elif len(yearList) > 2:
            if yearList[-2] in Year:
                year = yearList[-2]
        else:
            year = "NA"

        # print(d)
        # print('year:', year)
        # print('journal:', journal)
        # print('author:', author)
        # print('title:', title)

        text = author.replace(",", " ") + "," + title.replace(",", " ") + "," + journal.replace(",", " ") + "," + str(year)
        # 将各个字段合起来，组合成新的参考文献
        # 将每篇参考文献article加入文献集合Article
        if len(Articles) > 1:
            if text == Articles[-1]:
                continue
            else:
                Articles.append(text)
        else:
            Articles.append(text)
    return Articles

'''
统计每篇文献的被引次数,存入字典，并排序
'''
def countCitations(Articles):
    dicPapers = {}
    for paper in Articles:
        if paper in dicPapers.keys():
            dicPapers[paper] += 1
        else:
            dicPapers[paper] = 1
    # 将统计好被引次数的参考文献写入Article.csv中
    with open("year_cssci.csv", "a", encoding="utf8") as File:
        File.write("year" + "\t" + "CR"  + "\t" + "cited_times" + "\n")
        for paper_key in dicPapers:
            text_paper = paper_key.split(",")[3] + "\t" + paper_key + "\t" + str(dicPapers[paper_key])
            File.write(text_paper + "\n")



if os.path.isfile("cssci.txt"):
    print("-------------------------检测到CSSCI文件（cssci.txt），开始处理-------------------------" + '\n\n\n')
    data = readDataTxt("cssci.txt")
    Articles = getArticles(data)
    countCitations(Articles)
    print("-------------------------处理完成，请点击deduplication.exe对year_cssci.csv进行去重-------------------------" + '\n\n\n')
else:
    print('-------------------------未检测到cssci.txt-------------------------' + '\n\n\n')

if os.path.isfile("wos.txt"):
    print("-------------------------检测到WOS文件，开始处理(wos.txt)-------------------------" + '\n\n\n')
    Articles = []
    with open('wos.txt', 'r', encoding='utf8') as file:
        lines = file.readlines()
        for line in lines:
            # 参考文献
            cr = line.split('\t')[29]
            references = cr.split(';')
            for ref in references:
                if len(ref.split(',')) > 1:
                    if ref.split(',')[1].strip() in Year:
                        ref = ref + '|' + ref.split(',')[1].strip()
                        Articles.append(ref)
                    elif ref.split(',')[0].strip() in Year:
                        ref = ref + '|' + ref.split(',')[0].strip()
                        Articles.append(ref)

    #计算文章的被引频次
    dicPapers = {}
    for paper in Articles:
        if paper in dicPapers.keys():
            dicPapers[paper] += 1
        else:
            dicPapers[paper] = 1
    print('------------------------文章被引频次计算完成----------------------------'+ '\n\n\n')

    ArticleLines = []
    for key in dicPapers:
        ArticleLines.append(key.split("|")[1] + "\t" + key.split('|')[0] + "\t" + str(dicPapers[key]) + "\n")

    with open('year_wos.csv', 'a', encoding='utf8', newline='') as yearFile:
        yearFile.write("year\tCR\tcited times\n")
        for rs in ArticleLines:
            yearFile.write(rs)
    print("-------------------------处理完成，请点击deduplication.exe,对year_wos.csv进行去重-------------------------")

#     # 分年份将题录写成文件，这样做是为了提高下面相似度计算的速度
#     if os.path.exists("year"):
#         shutil.rmtree("year")
#         os.mkdir("year")
#     else:
#         os.mkdir("year")
#
#     for year in Year:
#         yearArticle = []
#         for key in dicPapers:
#             if key.split("|")[1] == year:
#                 yearArticle.append(key.split("|")[1] + "\t" + key.split('|')[0] + "\t" + str(dicPapers[key])+"\n")
#         if len(yearArticle) != 0:
#             print("写入文件：" + year + ".pp")
#             with open("year\\" +year + '.pp', 'a', encoding='utf8', newline='') as ffile:
#                 for rrow in yearArticle:
#                     ffile.write(rrow)
# # # 将统计好被引次数的参考文献写入Article.csv中
# # with open("Article.csv", "a", encoding="utf8") as File:
# #     File.write("year" + "\t" + "cited references" + "\t" + "cited_times" + "\n")
# #     for paper_key in dicPapers:
# #         text_paper = paper_key.split("|")[1] + "\t" + paper_key.split('|')[0] + "\t" + str(dicPapers[paper_key])
# #         File.write(text_paper + "\n")
# #
# # data_csv = pd.DataFrame(pd.read_csv("Article.csv", sep="\t", header=0))
# #
# # if os.path.exists("Article.csv"):
# #     os.remove("Article.csv")
# #
# # data_result = data_csv.sort_values(["year", "cited_times"], ascending=[True, False])
# # data_result.to_csv("year.csv", index= False, sep='\t', encoding="utf-8-sig",header=None)
#     NEW = []
#     for files in os.walk("year"):
#         for filename in files[2]:
#             print(filename)
#             texts = []
#             with open("year\\" + filename, 'r', encoding="utf8") as file:
#                 lines = file.readlines()
#                 for line in lines:
#                     texts.append(line.replace("\n", ''))
#             print("-----------------在对参考文献数据进行相似度计算、合并、去重，花费时间较多，请耐心等待-----------------------" + "\n")
#             while len(texts):
#                 NEW.append(deSame(texts))
#     # NEW = list(set(NEW))
#     # 当只有一篇文献的时候，会出现重复的现象，所以要进行去重
#     func = lambda x, y: x if y in x else x + [y]
#     reduce(func, [[], ] + NEW)
#     with open('year_wos.csv', 'a', encoding='utf8', newline='') as resultFile:
#         resultFile.write("year\tCR\tcited times\n")
#         for row in NEW:
#             resultFile.write(row + '\n')
#     print("-------------------------处理完成，请在根目录下查收year_wos.csv文件-------------------------")
#     shutil.rmtree("year")

else:
    print("-------------------------未检测到wos.txt-------------------------" + '\n\n\n')


