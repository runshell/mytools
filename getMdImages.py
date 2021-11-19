import requests
import re
import base64
import threading
import os


class markdown():
    def __init__(self,path):
        self.path=path
        with open(self.path,'r',encoding='utf8') as f:
            self.fileContent=f.read()
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        }

        pattern=r'![\[].*?[\]][(](https?://.*?)[)]'
        prog = re.compile(pattern)
        self.urls=prog.findall(self.fileContent)
        self.lock=threading.Lock()

    def getImage(self,url):
        print(url)
        try:
            imageBase64='data:image/png;base64,'+base64.b64encode(requests.get(url,headers=self.headers).content).decode('ascii')
        except Exception as e:
            print('\n\n',self.path,e,'\n\n')
        self.lock.acquire()
        self.fileContent=self.fileContent.replace(url,imageBase64)
        self.lock.release()
    def getImages(self):
        print(self.path,'start get images!')
        threads=[]
        for url in self.urls:
            threads.append(threading.Thread(target=self.getImage,args=(url,)))
            threads[-1].start()
        for thread in threads:
            thread.join()
        path=os.path.split(self.path)
        with open(os.path.join(path[0],'[img]'+path[1]),'w',encoding='utf8') as f:
            f.write(self.fileContent)
        print(self.path,'complete!')
        


def run(path):
    try:
        markdown(path).getImages()
    except Exception as e:
        print(e)

def getPath(path):
    paths=[]
    if os.path.isfile(path):
        paths=paths+[path]
    else:
        for dir in os.listdir(path):
            paths=paths+getPath(os.path.join(path,dir))
    return paths



if __name__=='__main__':
    threads=[]
    for md in getPath('.'):
        if os.path.isfile(md) and md.endswith('.md'):
            print(md)
            threads.append(threading.Thread(target=run,args=(md,)))
            threads[-1].start()
    for thread in threads:
        thread.join()
    print('All complete!')
