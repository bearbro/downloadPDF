import requests
import urllib3
import time
from requests.adapters import HTTPAdapter
def downloadPDF(name,url):
    #关闭ssl验证直接访问不安全链接，同时关闭报错
    requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    s = requests.Session()
    # s.mount('http://', HTTPAdapter(max_retries=3))
    # s.mount('https://', HTTPAdapter(max_retries=3))

    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D)\
     AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
    r = s.get(url,headers=headers,verify=False,timeout=(30,60))

    if r.status_code!=200:
        raise NameError(str(r.status_code))
    pdf = r.content       #响应的二进制文件
    with open(name,'wb') as f:     #二进制写入
        f.write(pdf)
    # print('完成')

    return

def writeFail(fail_log,content) :
    with open(fail_log, 'a+',encoding='UTF-8') as f:  # 二进制写入
        f.write(content+'\n')


#根据url下载pdf
if __name__=="__main__":
    fail_log="fail_log-utf"
    fail_n=0
    all_n=0

    #从数据库读取
    page='7'
    subN='6'
    name = 'Mysterium'
    url = 'https://www.aeternity.com/aeternity-blockchain-whitepaper.pdf'

    dir="1/"
    path=dir+page+"-"+subN+"-"+name+'.pdf'
    time_start = time.time()
    try :
        all_n += 1
        downloadPDF(path,url)
    except Exception as e:
        e_info = e.__class__.__name__
        if e_info=="NameError":
            e_info=str(e.args[0])
        print(e_info)
        writeFail(fail_log,path+' '+url+" "+e_info)
        fail_n+=1
    print("all:"+str(all_n)+"  succeed:"+str(all_n-fail_n)+"   fail:"+str(fail_n))
    time_end = time.time()
    usedtime = int(time_end - time_start)
    timelog = 'time cost:' + str(usedtime // 60) + "m" + str(usedtime % 60) + 's'
    print(timelog)
#page(1,2)/2-5-Bitpark Coin.pdf https://bitpark.net/BITPARK_whitepaper1.2.pdf