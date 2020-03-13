from multiprocessing.context import DefaultContext
from multiprocessing.process import BaseProcess
from typing import Optional, Callable, Any, Tuple, Mapping

import pyspider
import  bs4
import requests
import pymysql
import random
import multiprocessing
#里面的Process是大写的P
import time
    #关于bs4的用法最多的是findall直接返回的是一个set对象，要取得里面的子元素tag就必须要遍历（还可以数组一样按下标）。获得tag对象再使用
    #findall又可以进一步缩小范围    但是返回值带有标签  取text
    #不方便的是ide没有提示
'''
find_all()和find()都不好用，bs最好用的是select()，即CSS选择器。
你已经获取了一个大框架吧，比如它是soup中的一个Tag，然后：

results = tag.select('div[class="pro-detail-price"] span')
你这个例子里，results[0]就是这个指定的标签了。


'''



'''
对于数据库多线程的操作以及多进程的操作queue都可以作为中间操作应为他对于多进程以及多线程都是安全的可以后面单独设计一个程序
来让queue里面的数据写入数据库
还可以在操作数据库的部分加上进程锁以及线程锁但是   还是会出现一个进程独占的现象效果不好
'''
#爬取网站的URL可以按照此来开多个进程里面在开多线程
urldic={"国内高匿":"https://www.xicidaili.com/nn",
        "国内透明":"https://www.xicidaili.com/nt",
        "https代理":"https://www.xicidaili.com/wn",
        "http代理":"https://www.xicidaili.com/wt"
      }



#验证当前的ip是否可用
def validateIp(url,ip,port):
    try:
        proxy={"https":"https://"+ip+":"+str(port),"http":"http://"+ip+":"+str(port)}
        response=requests.get(url,proxies=proxy,verify=False,timeout=8,headers=getheaders())
        return  (response.status_code==requests.codes.ok)
    except Exception as e:
        print(e)
        return False

#需要带上head来请求
def getheaders():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers

#获取ip
def getOnepageIp(response):
    bs=bs4.BeautifulSoup(response.text,"lxml")
    c=bs.select("table")[0]
    d=c.select("tr")
    d.pop(0)
    for i in d:
        toip=i.select("td")
            #ip
        ip=toip[1].text
        print(ip)
        #port
        port=eval(toip[2].text)
        print(port)
        if (validateIp("https://www.cnblogs.com/selol/p/5446965.html", ip, port)):
                database(ip,port)



#获取所有ip
def getIp(url,host,port):
    try:
        proxy = {"https": "https://" + str(ipAndPortdic["host"]) + ":" + str(ipAndPortdic["port"]),
                "http": "http://" + str(ipAndPortdic["host"]) + ":" + str(ipAndPortdic["port"])}
        response = requests.get(url, proxies=proxy, verify=False, timeout=8, headers=getheaders())
    except Exception as e:
        print(e)
    bs=bs4.BeautifulSoup(response.text,"lxml")
    #bs4里面css选择器>前后都要加空格
    pagebar=bs.select("div.pagination > a")
    num=len(pagebar)
    allpagenum=pagebar[num-2].text
    for i in range(1,eval(allpagenum)+1):
        onepageurl=url+"/"+str(i)
        time.sleep(12)
        onepageresponse = requests.get(onepageurl, headers=getheaders())
        getOnepageIp(onepageresponse)
#把得到的ip写入数据库
def database(ip,port):
    #**********
    connect=pymysql.Connect(host='127.0.0.1', port=3308, user='root', password='zc19970919', db='ip', charset='utf8')
    try:
        cursor=connect.cursor()
        sql="insert into ip.iptable (ip_address,port) values ('%s',%d) on  duplicate  key update port=%d  "%(ip,port,port)
        cursor.execute(sql)
        print(cursor.lastrowid)
        #事务操作是由connect执行
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()



def getDatabaseIp():
    sql="select * from ip.iptable"
    connect=pymysql.connect(host='127.0.0.1',port=3308,user='root',password='zc19970919',db='ip',charset='utf8')
    try:
        cursor=connect.cursor()
        cursor.execute(sql)
        # 返回的是一个二维元组
        result=cursor.fetchall()
        resultList=[]
        for each in result:
            resultdic={}
            resultdic["host"]=each[1]
            resultdic["port"]=each[2]
            resultList.append(resultdic)
        return (random.choice(resultList))

    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':

    '''
    还没有多个ip所以单线程跑就行
    '''
    for each in urldic.values():
        #从数据库里面取出ip随机用一个访问  一个循环找出可以用的ip
        ipAndPortdic=getDatabaseIp()
        userful=validateIp('https://blog.csdn.net/qq_40625030/article/details/79722996',str(ipAndPortdic["host"]),ipAndPortdic["port"])
        while not  userful:
            ipAndPortdic = getDatabaseIp()
            userful = validateIp('https://blog.csdn.net/qq_40625030/article/details/79722996', str(ipAndPortdic["host"]),
                                 ipAndPortdic["port"])

        getIp(each,str(ipAndPortdic["host"]),ipAndPortdic["port"])
