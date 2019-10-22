import requests
from lxml import etree
import os

def escape_filename(name):
    return name.replace("/", "").replace('?', '')


class netease(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'

        }
        self.url = input("输入你要爬取歌单的id： ")
        self.url = "https://music.163.com/playlist?id="+self.url
        #self.url = "https://music.163.com/discover/toplist?id=3778678"
        self.url_list=[]
        self.name_list = []
    def getPage(self):
        res =requests.get(self.url,headers=self.headers).text
        html= etree.HTML(res)
        self.parsePage(html)
        print("获取界面完成")
    def parsePage(self,html):

        urls = html.xpath('//ul[@class="f-hide"]/li/a/@href')
        names=html.xpath('//ul[@class="f-hide"]/li/a/text()')

        for i in range(0,len(urls)):
            url = "http://music.163.com/song/media/outer/url" + str(urls[i][5:]) + ".mp3"
            self.url_list.append(url)
            name=str(names[i])+".mp3"
            self.name_list.append(name)
        print("解析完成")
    def show(self,contents):
        for content in contents:
            print(content)

    def downEase(self,url,name):
        print(url)
        music = requests.get(url,headers=self.headers)
        path1 = r'./music/'
        name = escape_filename(str(name))
        path = path1+name
        with open(path,"wb") as m:
             m.write(music.content)
             m.close()
        print("下载%s完成"%name)

        pass
    def workOn(self):
        self.getPage()
        for i in range(0,len(self.name_list)):
            print("开始下载第%d首歌%s"%(i,self.name_list[i]))
            self.downEase(self.url_list[i],self.name_list[i])
if __name__ == '__main__':
    #如果不存在的时候创建存储的文件夹 music
   if os.path.exists('./music/')==False:
        path1 = r'./music/'
        os.mkdir(path1)
   splider=netease()
   splider.workOn()
   print("全部下载完成")
