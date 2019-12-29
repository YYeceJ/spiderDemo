import requests
from bs4 import BeautifulSoup
import re
import pymysql

def insert(value):
    db = pymysql.connect("localhost", "root", "root", "zksdb", charset="utf8")
    cursor = db.cursor()
    sql = 'INSERT INTO department(name,parentId,introduction,isDeleted,note) VALUES (%s, %s, %s, %s, %s)'
    try:
        cursor.execute(sql, value)
        db.commit()
        print('插入成功')
    except:
        db.rollback()
        print('插入数据失败')
    db.close()

parentPertern = re.compile(r'<h4><a (.*?)>(.*?)&gt;</a></h4>',re.S)
sonPertern = re.compile(r'<span><a (.*?)>(.*?)</a></span>',re.S)
allPertern = re.compile(r'<li>(.*?)</li>',re.S)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
url = 'http://yyk.39.net/xian/'
res = requests.get(url,headers=headers)
print(res.status_code)
# 整页的HTML
soup = BeautifulSoup(res.text,'html.parser')
# 选取一段
soup = soup.find_all('ul',attrs={'class','lab-list clearfix'})
allArr = re.findall(allPertern,str(soup))
for inx,all in enumerate(allArr):
    parentDepartment = re.findall(parentPertern,all)
    parentDepartment = parentDepartment[0]
    parentDepartment = parentDepartment[1].strip()
    insert((parentDepartment,0,'',0,''))

    sonDepartmentSoup = BeautifulSoup(all,'html.parser')
    sonDepartment = sonDepartmentSoup.find_all('div',attrs={'class','lab-link'})
    sonDepartment = str(sonDepartment)
    sonDepartment = re.findall(sonPertern,sonDepartment)
    for index,item in enumerate(sonDepartment):
        sonDepartment = item[1].strip()
        field = (sonDepartment,inx + 1,'',0,'')
        insert(field)

