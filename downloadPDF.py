import requests
import pymysql
import os
import time
import urllib3
from sys import argv
from requests.adapters import HTTPAdapter

##更具url下载pdf并保存为name
def downloadPDF(name,url):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),name, "正在下载")
    # 关闭ssl验证直接访问不安全链接，同时关闭报错
    requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    #重试3次
    s = requests.Session()
    # s.mount('http://', HTTPAdapter(max_retries=3))
    # s.mount('https://', HTTPAdapter(max_retries=3))
    r = s.get(url, verify=False, timeout=(30,  60))

    if r.status_code!=200:
        raise NameError(str(r.status_code))
    pdf = r.content       #响应的二进制文件
    with open(name,'wb') as f:     #二进制写入
        f.write(pdf)
    # print('完成')

    return

##记录日志
def writeFail(fail_log,content) :
    with open(fail_log, 'a+',encoding='UTF-8') as f:  #
        f.write(content+'\n')



if __name__=="__main__":
    #下载【153，154）页的pdf
    minP, maxP = 153,154
    # 从命令行读取参数
    minP, maxP = int(argv[1]), int(argv[2])
    #日志文件名称
    fail_log="fail_log_"+"page["+str(minP)+","+str(maxP-1)+"]"
    fail_n=0
    all_n=0
    #保存pad的文件夹路径
    dir = "page(%s,%s)/" %( minP, maxP-1)
    #如果文件夹不存在则创建
    if not os.path.exists(dir):
        os.mkdir(dir)

    time_start = time.time()

    # 打开数据库连接
    # db = pymysql.connect("localhost", "root", "root", "icobenchdb")
    db = pymysql.connect("www.brobear.cc", "root", "root", "icobenchdb")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "SELECT page,subN,name,whitepaper_url,info_href from icos_url where page>=%s and page<%s order by page,subN" \
          % ( minP, maxP)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        page = row[0]
        subN = row[1]
        name = row[2]
        whitepaper_url = row[3]
        info_href = row[4]
        path = dir + str(page) + "-" + str(subN) + "-" + name + '.pdf'
        try:
            if not os.path.exists(path):
                all_n += 1
                downloadPDF(path, whitepaper_url)
        except Exception as e:
            e_info = e.__class__.__name__
            if e_info == "NameError":
                e_info = str(e.args[0])
            writeFail(fail_log,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\t' +e_info + '\t' +path + '\t'
                      + whitepaper_url+"\t"+info_href+"\t")
            fail_n += 1
        # 打印结果
        # print("page=%s\tsubN=%s\tname=%s\twhitepaper_url=%s" % (page, subN, name, whitepaper_url))

    # 关闭数据库连接
    db.close()
    # 构造日志信息
    time_end = time.time()
    usedtime=int(time_end - time_start)
    timelog='time cost:'+ str(usedtime//60)+"m"+str(usedtime%60)+'s'
    downloadlog="all:"+str(all_n)+"  succeed:"+str(all_n-fail_n)+"   fail:"+str(fail_n)
    pagelog="page:["+str(minP)+","+str(maxP-1)+"]"
    writeFail("log", pagelog)
    writeFail("log",timelog)
    writeFail("log", downloadlog)
    print(timelog)
    print(downloadlog)
