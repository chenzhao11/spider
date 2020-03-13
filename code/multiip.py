from multiprocessing.context import DefaultContext
from multiprocessing.process import BaseProcess
from typing import Optional, Callable, Any, Tuple, Mapping

import pyspider
import  bs4
import requests
import pymysql
import random
import queue
import traceback
import multiprocessing
#里面的Process是大写的P
from concurrent.futures import ThreadPoolExecutor
import time
    #关于bs4的用法最多的是findall直接返回的是一个set对象，要取得里面的子元素tag就必须要遍历（还可以数组一样按下标）。获得tag对象再使用
    #findall又可以进一步缩小范围    但是返回值带有标签  取text
    #不方便的是ide没有提示
'''
find_all()和find()都不好用，bs最好用的是select()，即CSS选择器。
你已经获取了一个大框架吧，比如它是soup中的一个Tag，然后：

results = tag.select('div[class="pro-detail-price"] span')
你这个例子里，results[0]就是这个指定的标签了。

对于数据库多线程的操作以及多进程的操作queue都可以作为中间操作应为他对于多进程以及多线程都是安全的可以后面单独设计一个程序
来让queue里面的数据写入数据库
还可以在操作数据库的部分加上进程锁以及线程锁但是   还是会出现一个进程独占的现象效果不好
'''

#用于输入到数据库里面使用的Queue


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
def getOnepageIp(response,databasequeue):
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
                dic={}
                dic["host"]=ip
                dic["port"]=port
                databasequeue.put(dic)



#获取所有ip
def getIp(url,ipfromdatabaselist,databasequeue):
    '''

    这里在拿到一个页面url过后 创建新的线程来跑每一个线程要求要自己到ip的queue里面自己取一个ip来跑
    :param url:
    :return:
    '''
    # 先哪一个代理ip取出首页入口
    ipAndPortdic=random.choice(ipfromdatabaselist)
    userful = validateIp('https://blog.csdn.net/qq_40625030/article/details/79722996', str(ipAndPortdic["host"]),
                         ipAndPortdic["port"])
    while not userful:
        ipAndPortdic = random.choice(ipfromdatabaselist)
        userful = validateIp('https://blog.csdn.net/qq_40625030/article/details/79722996', str(ipAndPortdic["host"]),
                             ipAndPortdic["port"])

    try:
        proxy = {"https": "https://" + str(ipAndPortdic["host"]) + ":" + str(ipAndPortdic["port"]),
                "http": "http://" + str(ipAndPortdic["host"]) + ":" + str(ipAndPortdic["port"])}
        response = requests.get(url, proxies=proxy, verify=False, timeout=8, headers=getheaders())
    except Exception as e:
        print(e)
    bs=bs4.BeautifulSoup(response.text,"lxml")
    #bs4里面css选择器>前后都要加空格      with 上下文管理协议
    pagebar=bs.select("div.pagination > a")
    num=len(pagebar)
    allpagenum=pagebar[num-2].text
    threadPool = ThreadPoolExecutor(max_workers=30)
    for i in range(1,eval(allpagenum)+1):
        threadPool.submit(actions(url,i,ipfromdatabaselist,databasequeue))



# 线程的action函数
def actions(url,i,ipfromdatabaselist,databasequeue):

    #先获取ip
    ipAndPortdic = random.choice(ipfromdatabaselist)
    userful = validateIp('https://blog.csdn.net/qq_40625030/article/details/79722996', str(ipAndPortdic["host"]),
                         ipAndPortdic["port"])
    while not userful:
        ipAndPortdic = random.choice(ipfromdatabaselist)
        userful = validateIp('https://blog.csdn.net/qq_40625030/article/details/79722996', str(ipAndPortdic["host"]),
                             ipAndPortdic["port"])

        onepageurl = url + "/" + str(i)
        # time.sleep(2)
        onepageresponse = requests.get(onepageurl, headers=getheaders())
        getOnepageIp(onepageresponse,databasequeue)


#把得到的ip写入数据库
def database(databasequeue):
        while True:
            connect=pymysql.Connect(host='127.0.0.1', port=3308, user='root', password='zc19970919', db='ip', charset='utf8')
            try:
                ipdic=databasequeue.get(block=True)
                ip=ipdic["host"]
                port=ipdic["port"]
                cursor=connect.cursor()
                sql="insert into ip.iptable (ip_address,port) values ('%s',%d) on  duplicate  key update port=%d  "%(ip,port,port)
                cursor.execute(sql)
                print(cursor.lastrowid)
                #事务操作是由connect执行
                connect.commit()
            except Exception as e:
                # *******************************************************
                print(traceback.format_exc())
                connect.rollback()



def getDatabaseIpList():
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
        return resultList

    except Exception as e:
        traceback.print_exc()

#多进程方法一   还可以直接使用pool （用pool能保证线程安全么？）
class MyProcess(multiprocessing.Process):
    def __init__(self,name,url,iplist,resultqueqeu):
        super().__init__()
        self.name=name
        self.url=url
        self.ipfromdatabaselist=iplist
        self.databasequeue=resultqueqeu
    # def __init__(self,name,url):
    #     super().__init__()
    #     self.name=name
    #     self.url=url

    def run(self) :
        try:
            ipAndPortdic = random.choice(self.ipfromdatabaselist)
            userful = validateIp('https://blog.csdn.net/qq_40625030/article/details/79722996', str(ipAndPortdic["host"]),
                                ipAndPortdic["port"])
            while not userful:
                ipAndPortdic = random.choice(self.ipfromdatabaselist)
                userful = validateIp('https://blog.csdn.net/qq_40625030/article/details/79722996',
                                    str(ipAndPortdic["host"]),
                                    ipAndPortdic["port"])
            proxy = {"https": "https://" + str(ipAndPortdic["host"]) + ":" + str(ipAndPortdic["port"]),
                     "http": "http://" + str(ipAndPortdic["host"]) + ":" + str(ipAndPortdic["port"])}
            response = requests.get(self.url, proxies=proxy, verify=False, timeout=8, headers=getheaders())
            bs = bs4.BeautifulSoup(response.text, "lxml")
            # bs4里面css选择器>前后都要加空格      with 上下文管理协议

            pagebar = bs.select("div.pagination > a")
            num = len(pagebar)
            allpagenum = pagebar[num - 2].text
        except Exception as e:
            print(e)
            self.run()
        threadPool = ThreadPoolExecutor(max_workers=30)
        for i in range(1, eval(allpagenum) + 1):
            future=threadPool.submit(actions(self.url,i,self.ipfromdatabaselist,self.databasequeue))
            print(self.name)
            print(type(future))

class MyDatabaseProcess(multiprocessing.Process):

    def __init__(self,name,databasequeue):
        super().__init__()
        self.name=name
        self.databasequeue=databasequeue
    def run(self):
        database(self.databasequeue)


if __name__ == '__main__':
    # ************************声明多进程的变量要到main函数****************************************************
    databasequeue = multiprocessing.Manager().Queue()
    ipfromdatabaselist = multiprocessing.Manager().list()
    ipfromdatabaselist=getDatabaseIpList()
    process=[]
    urllist=list(urldic.values())
    process1=MyProcess(name="process1",url=urllist[0],iplist=ipfromdatabaselist,resultqueqeu=databasequeue)
    process2 = MyProcess(name="process2",url=urllist[1],iplist=ipfromdatabaselist,resultqueqeu=databasequeue)
    process3 = MyProcess(name="process3",url=urllist[2],iplist=ipfromdatabaselist,resultqueqeu=databasequeue)
    process4 = MyProcess(name="process4",url=urllist[3],iplist=ipfromdatabaselist,resultqueqeu=databasequeue)
    databaseProcess=MyDatabaseProcess("databaseProcess",databasequeue)
    # process.append(process1)
    # process.append(process2)
    # process.append(process3)
    # process.append(process4)
    # process.append(databaseProcess)
    # start开始  run是不指定target默认执行的

    process1.start()
    print("线程1开始")
    process2.start()
    print("线程2开始")
    process3.start()
    print("线程3开始")
    process4.start()
    print("线程4开始")
    databaseProcess.start()
    # 要加上join让主线程等待子线程    保持connection  才能访问里面的connection
    process1.join()
    print("线程1结束")
    process2.join()
    print("线程2结束")
    process3.join()
    print("线程3结束")
    process4.join()
    print("线程4结束")
    if (not (process1.is_alive() or process2.is_alive() or process3.is_alive() or process4.is_alive())):
        databaseProcess.close()
    databaseProcess.join()
    print("全部结束，停止写入数据库！")





