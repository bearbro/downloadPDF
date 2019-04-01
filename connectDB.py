#!/usr/bin/python3

import pymysql

##连接数据库的一个测试
if __name__=="__main__":
    # 打开数据库连接
    # db = pymysql.connect("localhist", "root", "root", "icobenchdb")
    db = pymysql.connect("www.brobear.cc", "root", "root", "icobenchdb")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    minP, maxP=4,8
    # 使用 execute()  方法执行 SQL 查询
    sql="SELECT page,subN,name,whitepaper_url from icos_url where page>=%s and page<%s order by page,subN" % (minP,maxP)
    cursor.execute(sql)

    results = cursor.fetchall()
    for row in results:
        page = row[0]
        subN = row[1]
        name = row[2]
        whitepaper_url = row[3]
        # 打印结果
        print("page=%s\tsubN=%s\tname=%s\twhitepaper_url=%s" % (page, subN, name, whitepaper_url))

    # 关闭数据库连接
    db.close()
