# -*- encoding=UTF-8 -*-
def test_string():
    str = "hello"
    str1 = "world!"
    # print (1,str)
    # print 2,str+str1
    # print  3,str.upper()
    # print  4,str.capitalize()
    # print  5,str.center(20,"-")
    print  "x".join(['1', '2', '3'])
    str2 = str.join(str1)
    print  6, str2.endswith("orld!")
    print  7, str2
    print len(str1), len(str), len(str2)
    # split函数把前面字符串按照给定模式分隔    给定的字符串 是说的最大可以匹配多少个  分隔符
    stra = "aaa_aaaa_bbbb_ccc"
    print 8, stra.split("_")
    print 9, stra.split("_", 1)
    print 10, stra.split("_", 2)
    # join是把调用join的字符串加入到后面itreable对象每一个itreate后面  实现把后面的用指定的符号
    # 连接起来
    print 11, 'x'.join(["hello world ", " zc"])
    strd = " \r\n hello world! \r\n"
    strc = "   zczczc hello"
    # ltrip   rtrip 要是有指定的模式 删除以其开头的串，，不指定默认返回去掉开头空格的
    # 要是不是默认的，那串必须完全匹配
    print 12, strd
    print 13, strd.lstrip(" \r\n")
    print 14, strc.strip()
    print 15, strc.strip("   zc")
    print 16, strc.replace("zc", "cy", 2)


def demo_opreation():
    print 17, 1 | 0, 0 | 0, 1 & 6, 1 & 0, 1 ^ 2
    print type(True | False)
    print 18, 1 << 3, 16 >> 3


def demo_buildinfunction():
    # divmod 求商以及对应的余数
    print 1, divmod(16, 3)
    print 2, abs(-9), abs(9)
    print 3, chr(67), ord("A")
    # eval可以用来执行脚本
    print 4, eval("6*6*6")
    print 5, range(0, 10)
    print 6, range(0, 100, 20)


def demo_controfollow():
    for i in range(0, 10):
        print 1, i
        if i == 5:
            print "test if"
        elif i == 6:
            print "test elseif"
    print 2, i
    # for 循环里面的i 不用提前定义   使用后后面的都可以用i要是在循环外面使用i会是上次的值
    # while使用的变量之前必须有定义
    j = 0
    while j < 20:
        print 3, j
        j = j + 2

    print 4, j
    for i in range(0, 10):
        print 5, i


def demo_list():
    #定义一个list直接用name=[]  要是用的（）就是不可以更改的list
    lista = [1, 2, 3]
    listb = ["a", 4, 5, 6]
    print 1, lista
    listc = lista + listb
    print 2, listc
    listb.append("hahah")
    print 3,listb
    #count计算list里面有指定的元素多少个     对于list的操作一般都没有返回值

    print 4, listb.count(11)
    listb.extend(["extend"])
    print 5,listb
    listb.reverse()
    print 6,listb
    print 7,listb.pop(2)
    listb.insert(2, "insert")
    print 8,listb
    listd=["hello"]
    #*10不会对于list的内容改变
    print 9,listd*10
    liste=(0,1,2)
    print 10,liste.count(1)
def demo_dict():
    dic1={1:2,2:3,"hello":"world"}
    print 1,dic1.keys()
    print  2,dic1.values()
    print 3,dic1.items()
    for key ,value in dic1.items():
        print 4,key,value
    for keyandvalue in dic1.items():
        print 5,keyandvalue
    for i in dic1.keys():
        print 6,i
    dicb={"add":"+","sub":"-"}
    #字典就是一个key_value键值对   添加使用的是dic【】= 类似数组    删除使用pop or del
    del dicb["add"]
    dicb["hello"]="zc"
    dicb["3"]="hahhah"
    print 7,dicb
    print 8,dicb.pop("3")
    print 9, dicb


#set集合主要还是用来求交并补集合的工具
def demo_set():
    lista=[1,2,3,4,5]
    #定义set的方法特别  name=set(可遍历对象)
    seta=set(lista)
    setb=set([4,5,6,8,9])
    setc=set((7,8,9,1,2))
    print 1,seta
    print 2,setb
    print 3,setc
    #intersection 求交集 与 &是一样的
    sete=seta.intersection(setb)
    print 4,sete
    #+不行但是-可以求出a除去b余下的
    print 5,seta-setb,setb-seta
    print 6,seta & setb
    #或与union是一样的
    print 7,seta |setb,seta.union(setb)
    #亦或^除去两个里面相同的     留下不一样的元素
    print 8,seta ^setb
    #isdisjoint 判断是不是完全不相交的两个集合
    print 9 ,seta.isdisjoint(setb)
    seta.add("hahhaha")
    print 10,seta


if __name__ == '__main__':
    # test_string()
    # demo_opreation()
    # demo_buildinfunctio()
    # demo_controfollow()
    # demo_list()
    # demo_dict()
    demo_set()