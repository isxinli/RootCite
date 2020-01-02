
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import os
import time
import sys
import os
import re


def dict2list(dic: dict):
    """ 将字典转化为列表 """
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst


Year = ['1700', '1701', '1702', '1703', '1704', '1705', '1706', '1707', '1708', '1709', '1710', '1711', '1712',
        '1713',
        '1714', '1715', '1716', '1717', '1718', '1719', '1720', '1721', '1722', '1723', '1724', '1725', '1726',
        '1727',
        '1728', '1729', '1730', '1731', '1732', '1733', '1734', '1735', '1736', '1737', '1738', '1739', '1740',
        '1741',
        '1742', '1743', '1744', '1745', '1746', '1747', '1748', '1749', '1750', '1751', '1752', '1753', '1754',
        '1755',
        '1756', '1757', '1758', '1759', '1760', '1761', '1762', '1763', '1764', '1765', '1766', '1767', '1768',
        '1769',
        '1770', '1771', '1772', '1773', '1774', '1775', '1776', '1777', '1778', '1779', '1780', '1781', '1782',
        '1783',
        '1784', '1785', '1786', '1787', '1788', '1789', '1790', '1791', '1792', '1793', '1794', '1795', '1796',
        '1797',
        '1798', '1799', '1800', '1801', '1802', '1803', '1804', '1805', '1806', '1807', '1808', '1809', '1810',
        '1811',
        '1812', '1813', '1814', '1815', '1816', '1817', '1818', '1819', '1820', '1821', '1822', '1823', '1824',
        '1825',
        '1826', '1827', '1828', '1829', '1830', '1831', '1832', '1833', '1834', '1835', '1836', '1837', '1838',
        '1839',
        '1840', '1841', '1842', '1843', '1844', '1845', '1846', '1847', '1848', '1849', '1850', '1851', '1852',
        '1853',
        '1854', '1855', '1856', '1857', '1858', '1859', '1860', '1861', '1862', '1863', '1864', '1865', '1866',
        '1867',
        '1868', '1869', '1870', '1871', '1872', '1873', '1874', '1875', '1876', '1877', '1878', '1879', '1880',
        '1881',
        '1882', '1883', '1884', '1885', '1886', '1887', '1888', '1889', '1890', '1891', '1892', '1893', '1894',
        '1895',
        '1896', '1897', '1898', '1899', '1900', '1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908',
        '1909',
        '1910', '1911', '1912', '1913', '1914', '1915', '1916', '1917', '1918', '1919', '1920', '1921', '1922',
        '1923',
        '1924', '1925', '1926', '1927', '1928', '1929', '1930', '1931', '1932', '1933', '1934', '1935', '1936',
        '1937',
        '1938', '1939', '1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', '1950',
        '1951',
        '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963', '1964',
        '1965',
        '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978',
        '1979',
        '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992',
        '1993',
        '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
        '2007',
        '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

class SThread(QThread):
    Signal = pyqtSignal(str)

    def __init__(self,parent=None):
        print("sdjahdha")

        super(SThread, self).__init__(parent)
    def run(self):
            print("sdjahdha")
            sys.setrecursionlimit(10000000)
            thisPath = os.getcwd()
            cssci_path = thisPath + "\\\\" + "RootCiteProject" + "\\\\" + 'cssci.txt'
            wos_path = thisPath + "\\\\" + "RootCiteProject" + "\\\\" + 'wos.txt'

            if os.path.isfile(cssci_path):
                print("-------------------------检测到CSSCI文件（cssci.txt），开始处理-------------------------" + '\n\n')
                # 将所有文献存入data列表，列表的每个元素是一篇文献，以原来的参考文献的格式保存
                data = []
                #  读取文件
                print("-------------------------读取文件中-------------------------" + '\n\n')

                with open(cssci_path, encoding="utf8") as dataFile:
                    while 1:
                        line = dataFile.readline()
                        if not line:
                            break
                        if line.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
                            data.append(line.replace("\n", ""))

                #  将文件格式转换为标准格式，并以“作者|标题|期刊|发表年份”的格式一依次存入Articles列表
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

                    text = author.replace(",", " ") + "," + title.replace(",", " ") + "," + journal.replace(",",
                                                                                                            " ") + "|" + str(
                        year)
                    # 将各个字段合起来，组合成新的参考文献
                    # 将每篇参考文献article加入文献集合Article
                    if len(Articles) > 1:
                        if text == Articles[-1]:
                            continue
                        else:
                            Articles.append(text)
                    else:
                        Articles.append(text)

                #  文件处理
                dicPapers = {}
                dicYear = {}
                print("-------------------------文件处理中-------------------------" + '\n\n')
                for paper in Articles:
                    p = paper.split("|")
                    key = p[0]
                    if key in dicPapers.keys():
                        dicPapers[key] += 1
                    else:
                        dicPapers[key] = 1
                    key_year = p[1]
                    if key_year in dicYear.keys():
                        dicYear[key_year] += 1
                    else:
                        dicYear[key_year] = 1

                # 对字典按年份排序
                dic1 = sorted(dict2list(dicYear), key=lambda x: x[0], reverse=False)

                #  生成rpys.csv文件
                print("-------------------------生成rpys文件中-------------------------" + '\n\n')
                Result = []
                yearExist = []
                for j in dic1:
                    yearExist.append(j[0])
                for x in Year:
                    if x in yearExist:
                        result = x + "," + str(dicYear[x]) + "\n"
                    else:
                        result = x + "," + str(0) + "\n"
                    Result.append(result)

                with open(thisPath + "\\" + "RootCiteProject" + "\\" + "rpys_cssci.csv", "a",
                          encoding="utf8") as resultFile:
                    for rs in Result:
                        resultFile.write(rs)

                # 生成median.csv文件
                print("-------------------------生成median文件中-------------------------" + '\n\n')
                Median = []
                times = []
                for time in Result:
                    times.append(time.split(",")[1].replace("\n", ""))
                # 计算平均偏差
                count = 2
                for yy in range(2, len(times[:-3])):
                    ss = int(times[count - 2]) + int(times[count - 1]) + int(times[count]) + int(
                        times[count + 1]) + int(
                        times[count + 2])
                    avg = ss / 5
                    median = round((float(times[count]) - avg), 3)
                    Median.append(median)
                    count += 1

                MedianResult = []
                for indexCount in range(2, (len(Result) - 3)):
                    medianRs = Result[indexCount].replace("\n", "") + "," + str(Median[indexCount - 2])
                    MedianResult.append(medianRs)

                medianList1 = ['1700,0,0.0', '1701,0,0.0']
                medianList2 = ['2018,0,0.0', '2019,0,0.0', '2020,0,0.0']
                MedianResult = medianList1 + MedianResult + medianList2

                with open(thisPath + "\\" + "RootCiteProject" + "\\" + "median_cssci.csv", "a",
                          encoding="utf8") as MedianResultFile:
                    for mrs in MedianResult:
                        MedianResultFile.write(mrs + "\n")

            else:
                print("-------------------------未检测cssci.txt-------------------------" + '\n\n')

            if os.path.isfile(wos_path):
                print("-------------------------检测到WOS文件，开始处理(wos.txt)-------------------------" + '\n\n')
                Articles = []
                with open(wos_path, 'r', encoding='utf8') as file:
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

                #  文件处理
                dicPapers = {}
                dicYear = {}
                print("-------------------------文件处理中-------------------------" + '\n\n')
                for paper in Articles:
                    p = paper.split("|")
                    key = p[0]
                    if key in dicPapers.keys():
                        dicPapers[key] += 1
                    else:
                        dicPapers[key] = 1
                    key_year = p[1]
                    if key_year in dicYear.keys():
                        dicYear[key_year] += 1
                    else:
                        dicYear[key_year] = 1

                # 对字典按年份排序
                dic1 = sorted(dict2list(dicYear), key=lambda x: x[0], reverse=False)

                #  生成rpys.csv文件
                print("-------------------------生成rpys文件中-------------------------" + '\n\n')
                Result = []
                yearExist = []
                for j in dic1:
                    yearExist.append(j[0])
                for x in Year:
                    if x in yearExist:
                        result = x + "," + str(dicYear[x]) + "\n"
                    else:
                        result = x + "," + str(0) + "\n"
                    Result.append(result)

                with open(thisPath + "\\" + "RootCiteProject" + "\\" + "rpys_wos.csv", "a",
                          encoding="utf8") as resultFile:
                    for rs in Result:
                        resultFile.write(rs)

                # 生成median.csv文件
                print("-------------------------生成median文件中-------------------------" + '\n\n')
                Median = []
                times = []
                for time in Result:
                    times.append(time.split(",")[1].replace("\n", ""))
                # 计算平均偏差
                count = 2
                for yy in range(2, len(times[:-3])):
                    ss = int(times[count - 2]) + int(times[count - 1]) + int(times[count]) + int(
                        times[count + 1]) + int(
                        times[count + 2])
                    avg = ss / 5
                    median = round((float(times[count]) - avg), 3)
                    Median.append(median)
                    count += 1

                MedianResult = []
                for indexCount in range(2, (len(Result) - 3)):
                    medianRs = Result[indexCount].replace("\n", "") + "," + str(Median[indexCount - 2])
                    MedianResult.append(medianRs)

                medianList1 = ['1700,0,0.0', '1701,0,0.0']
                medianList2 = ['2018,0,0,0.0', '2019,0,0.0', '2020,0,0.0']
                MedianResult = medianList1 + MedianResult + medianList2

                with open(thisPath + "\\\\" + "RootCiteProject" + "\\\\" + "median_wos.csv", "a",
                          encoding="utf8") as MedianResultFile:
                    for mrs in MedianResult:
                        MedianResultFile.write(mrs + "\n")


            else:
                print("-------------------------未检测到wos.txt-------------------------" + '\n\n')
                #time.sleep(20)



            print("###################")

            # time.sleep(3)






