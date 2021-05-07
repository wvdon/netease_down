import requests
from lxml import etree
import os
import json
def escape_filename(name):
    return name.replace("/", "").replace('?', '')


class netease(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'

        }
        self.url=""
        self.url_list=[]
        self.name_list = []

    def parseHow(self):
        self.url = input("本系统可以爬取指定歌单的所有歌曲，或者下载单首歌曲"
                         "\n 输入你要爬取歌单或者歌曲的链接：\n")
        # self.url= "https://music.163.com/playlist?id=6745481740"

        if  self.url[24]=='s' or self.url[22]=='s':
            self.url_list.append("https://tenapi.cn/wyyinfo/?id=" +self.url[-10:])

            html = requests.get(self.url_list[0],self.headers).text
            name = json.loads(html)['data']['songs']
            self.name_list.append(name+".mp3")
            self.downEase("http://music.163.com/song/media/outer/url"+self.url[-10:]+".mp3",self.name_list[0])
        else:
            self.url = "https://music.163.com/playlist?id="+self.url[-10:]
            self.workOn()


    def getPlayListMusic(self):
        self.url = "https://music.163.com/playlist?id=" + self.url[-7:]

    def getPage(self,url,headers):
        res =requests.get(url,headers=self.headers)
        if res.status_code != 200:
            print("获取失败")
        else:
            html = etree.HTML(res.text)
            print("获取界面完成")
            return html

    def parsePage(self):
        html = self.getPage(self.url,self.headers)
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
        music = requests.get(url,headers=self.headers)
        path1 = r"./music/"
        name = escape_filename(str(name))
        path = path1+name
        with open(path,"wb") as m:
             m.write(music.content)
             m.close()
        print("下载%s完成"%name)

    def workOn(self):
        self.getPage(self.url,self.headers)
        self.parsePage()
        for i in range(0,len(self.name_list)):
            print("开始下载第%d首歌%s"%(i+1,self.name_list[i]))
            self.downEase(self.url_list[i],self.name_list[i])

    def run(self):
        self.parseHow()

if __name__ == '__main__':
    #如果不存在的时候创建存储的文件夹 music
   if os.path.exists('./music/')==False:
        path1 = r'./music/'
        os.mkdir(path1)

   splider=netease()
   splider.run()
   print("全部下载完成")
