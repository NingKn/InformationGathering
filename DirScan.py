#coding:utf-8
import optparse
import requests
import threading
import time
import sys

time_start=time.time()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Connection':'close'
           }

class mythread(threading.Thread):
    def __init__(self,urlScan,newDir):
        threading.Thread.__init__(self)
        self._urlScan=urlScan
        self._newDir=newDir
    def run(self):
        print(threading.current_thread(),'is up')
        for text in self._newDir:
            link=self._urlScan+'/'+text
            try:
                conn = requests.get(link, headers=headers,stream=True)
                if conn.status_code == 200:
                    print(link + str(conn))
            except requests.exceptions.ConnectionError as e:
                print(e)

def startScan(urlScan,Num,wordlist):
    threadList = []
    dir = []
    a = []
    newDir = []
    with open(wordlist, 'r') as f:
        for txt in f:
            txt = txt.replace('\n', '')
            dir.append(txt)

    Num=int(Num)
    Len=int(len(dir)/Num)
    for i in range(1,Num+1):
        for j in range((i-1)*Len,i*Len):
            a.append(dir[j])
        if i!=Num:
            newDir.append(a[(i - 1) * Len:i * Len])
        else:
            newDir.append(dir[(i - 1) * Len:])

    for i in range(Num):
        threadList.append(mythread(urlScan,newDir[i]))
    for thread in threadList:
        thread.start()
    for thread in threadList:
        thread.join()
    time_end = time.time()
    print('耗时：', time_end - time_start)

if __name__ == '__main__':
    try:
        parse=optparse.OptionParser('%prog -u http://127.0.0.1 -w test.txt -t 10')
        parse.add_option('-u',dest='urlScan')
        parse.add_option('-t',dest='threadNum',default=10)
        parse.add_option('-w',dest='wordlist')
        options,args=parse.parse_args()
        startScan(options.urlScan,options.threadNum,options.wordlist)
    except TypeError:
        print('python3 DirScan.py -u http://127.0.0.1 -w test.txt -t 10')







