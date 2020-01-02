from PyQt5.QtWidgets import QApplication, QMainWindow, qApp,QStyleFactory
from PyQt5 import QtCore, QtGui, QtWidgets

from datasketch import MinHashLSH, MinHash
import time
import sys
import os
import re

from MyThread import SThread
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


# 删除文件夹下的所有文件和文件夹
def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)


# 对字典排序前需要把字典转化为列表
def dict2list(dic: dict):
    """ 将字典转化为列表 """
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst


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

        text = author.replace(",", " ") + "," + title.replace(",", " ") + "," + journal.replace(",", " ") + "," + str(
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
    return Articles


def countCitations(Articles):
    thisPath = os.getcwd()
    dicPapers = {}
    for paper in Articles:
        if paper in dicPapers.keys():
            dicPapers[paper] += 1
        else:
            dicPapers[paper] = 1
    # 将统计好被引次数的参考文献写入Article.csv中
    with open(thisPath + "\\" + "RootCiteProject" + "\\" + "year_cssci.csv", "a", encoding="utf8") as File:
        File.write("year" + "\t" + "CR" + "\t" + "cited_times" + "\n")
        for paper_key in dicPapers:
            text_paper = paper_key.split(",")[3] + "\t" + paper_key + "\t" + str(dicPapers[paper_key])
            File.write(text_paper + "\n")


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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Welcome to RootCite1.0")
        MainWindow.resize(616, 462)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 20, 431, 361))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(1000, 1000))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 441, 1001))
        self.textEdit.setObjectName("textEdit")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(490, 30, 91, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(490, 100, 91, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(490, 150, 91, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(490, 220, 91, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(490, 270, 91, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(490, 340, 91, 41))
        self.pushButton_6.setObjectName("pushButton_6")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 390, 241, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(480, 10, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(480, 80, 81, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(480, 200, 54, 12))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(480, 320, 81, 16))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Welcome to RootCite1.0"))
        self.pushButton.setText(_translate("MainWindow", "create"))
        self.pushButton_2.setText(_translate("MainWindow", "readCSSCI"))
        self.pushButton_3.setText(_translate("MainWindow", "readWOS"))
        self.pushButton_4.setText(_translate("MainWindow", "rpys"))
        self.pushButton_5.setText(_translate("MainWindow", "year"))
        self.pushButton_6.setText(_translate("MainWindow", "deduplication"))
        self.label.setText(_translate("MainWindow", "All rights reserved by PyAcademic@2018."))
        self.label_2.setText(_translate("MainWindow", "file"))
        self.label_3.setText(_translate("MainWindow", "preprocessing"))
        self.label_4.setText(_translate("MainWindow", "rpys"))
        self.label_5.setText(_translate("MainWindow", "deduplication"))


class MyPyQT_Form(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyPyQT_Form, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open)
        self.pushButton_2.clicked.connect(self.readCSSCI)
        self.pushButton_3.clicked.connect(self.readWOS)
        self.pushButton_4.clicked.connect(self.rpys)
        self.pushButton_5.clicked.connect(self.year)
        self.pushButton_6.clicked.connect(self.deduplication)
        self.textEdit.append("\n*********************************************\n"
                             "*********************************************\n"
                             "*********************************************\n\nWelcome to "
                             "RootCite1.0\n\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                             "\n\n*********************************************\n"
                             "*********************************************\n"
                             "*********************************************\n""\n")
        self.thread = SThread()
        sys.setrecursionlimit(10000000)


        self.show()

    # 实现pushButton_click()函数，textEdit是我们放上去的文本框的id
    def open(self):
        thisPath = os.getcwd()
        filename = thisPath.replace("\\", "\\\\") + "\\\\RootCiteProject"
        if os.path.exists(filename):
            del_file(filename)
        else:
            os.mkdir(filename)
            os.mkdir(filename + "\\\\data_cssci")
            os.mkdir(filename + "\\\\data_wos")
        self.textEdit.append(
            "在当前目录下创建工程成功！\n\n请将Web of Science和CSSCI下载的单个或多个\n题录文件分别放入文件夹data_wos和data_cssci文件夹。\n\n" + time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime()) + "\n*********************************************")

    def readCSSCI(self):
        rows = []
        thisPath = os.getcwd()
        path = thisPath.replace("\\", "\\\\") + "\\\\" + "RootCiteProject" + "\\\\data_cssci"

        for files in os.walk(path):
            for filename in files[2]:
                print(filename)
                self.textEdit.append("正在读取" + filename + "\n")
                with open(path + "\\\\" + filename, 'r', encoding="utf8") as file:
                    lines = file.readlines()
                    for line in lines:
                        rows.append(line)

        with open(thisPath + "\\\\" + "RootCiteProject" + "\\\\" + 'cssci.txt', 'a', encoding="utf8") as file1:
            for rs in rows:
                file1.write(rs)

        self.textEdit.append("\n\n读取CSSCI题录数据成功！\n\n" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                      time.localtime()) + "\n*********************************************")

    def readWOS(self):
        rows = []
        thisPath = os.getcwd()
        path = thisPath.replace("\\", "\\\\") + "\\\\RootCiteProject" + "\\\\data_wos"

        for files in os.walk(path):
            for filename in files[2]:
                print(filename)
                self.textEdit.append("正在读取" + filename + "\n")
                with open(path + "\\" + filename, 'r', encoding='utf8') as file:
                    lines = file.readlines()
                    for line in lines:
                        row = re.split('[\t]', line)[:-1]
                        rows.append(row)

        with open(thisPath + "\\\\" + "RootCiteProject" + "\\\\" + 'wos.txt', 'a', encoding='utf8',
                  newline='') as file1:
            for rs in rows:
                rs = '\t'.join(rs)
                # print(rs)
                file1.write(rs + '\n')

        self.textEdit.append("\n\n已点击readWOS按钮，读取Web of Science题录数据成功!\n\n" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                            time.localtime()) + "\n*********************************************")





    def rpys(self):

       self.thread.start()

       self.textEdit.append("\n\nRPYS文件生成成功！请查收rpys和median文件！\n\n" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                   time.localtime()) + "\n*********************************************")
    def year(self):
        thisPath = os.getcwd()
        cssci_path = thisPath + "\\" + "RootCiteProject" + "\\" + 'cssci.txt'
        wos_path = thisPath + "\\" + "RootCiteProject" + "\\" + 'wos.txt'

        if os.path.isfile(cssci_path):
            print("-------------------------检测到CSSCI文件（cssci.txt），开始处理-------------------------" + '\n\n\n')
            data = readDataTxt(cssci_path)
            Articles = getArticles(data)
            countCitations(Articles)
            print(
                "-------------------------处理完成，请点击deduplication.exe对year_cssci.csv进行去重-------------------------" + '\n\n\n')
        else:
            print('-------------------------未检测到cssci.txt-------------------------' + '\n\n\n')

        if os.path.isfile(wos_path):
            print("-------------------------检测到WOS文件，开始处理(wos.txt)-------------------------" + '\n\n\n')
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

            # 计算文章的被引频次
            dicPapers = {}
            for paper in Articles:
                if paper in dicPapers.keys():
                    dicPapers[paper] += 1
                else:
                    dicPapers[paper] = 1
            print('------------------------文章被引频次计算完成----------------------------' + '\n\n\n')

            ArticleLines = []
            for key in dicPapers:
                ArticleLines.append(key.split("|")[1] + "\t" + key.split('|')[0] + "\t" + str(dicPapers[key]) + "\n")

            with open(thisPath + "\\" + "RootCiteProject" + "\\" + 'year_wos.csv', 'a', encoding='utf8',
                      newline='') as yearFile:
                yearFile.write("year\tCR\tcited times\n")
                for rs in ArticleLines:
                    yearFile.write(rs)
            print("-------------------------处理完成，请点击deduplication.exe,对year_wos.csv进行去重-------------------------")
        else:
            print("-------------------------未检测到wos.txt-------------------------" + '\n\n\n')
        self.textEdit.append("\n\n已点击year按钮，year文件计算完成，请查收！\n\n" + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                 time.localtime()) + "\n*********************************************")

    def deduplication(self):
        thisPath = os.getcwd()
        cssci_path = thisPath + "\\" + "RootCiteProject" + "\\" + 'year_cssci.csv'
        wos_path = thisPath + "\\" + "RootCiteProject" + "\\" + 'wos.txt'
        result_cssci_path = thisPath + "\\" + "RootCiteProject" + "\\" + 'result_cssci.csv'
        result_wos_path = thisPath + "\\" + "RootCiteProject" + "\\" + 'result_wos.csv'

        if os.path.isfile(cssci_path):
            deduplication(cssci_path, result_cssci_path)
            os.remove(cssci_path)
        else:
            print("请先点击rpys和year生成初始结果")
        if os.path.isfile(wos_path):
            deduplication(wos_path, result_wos_path)
            os.remove(wos_path)
        else:
            print("请先点击rpys和year生成初始结果")

        print('-------------------处理完成，请在根目录下查收result_CSSCI.csv、result_WOS.csv文件进行分析-------------------------')

        self.textEdit.append(
            "\n\n已点击deduplication按钮，去重花费时间较多，请喝一杯咖啡小憩一下吧！\n\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


if __name__ == '__main__':
    app = QApplication(sys.argv)


    #with open(r"style.qss", 'r') as styleSheet:
       # app.setStyleSheet(styleSheet.read())



    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())

