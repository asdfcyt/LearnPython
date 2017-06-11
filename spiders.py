# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from jianshu.items import InformationItem, FanListItem
from jianshu.items import FollowColletionItem, LikeArticleItem, FollowListItem
import re
from bs4 import BeautifulSoup

class Spider(CrawlSpider):
    name = "jianshu"
    host = "http://www.jianshu.com"

    start = ["a987b338c373", "9104ebf5e177", "d83382d92519", "71a1df9e98f6","6c9580370539","65b9e2d90f5b","9d275c04c96c","a0d5c3ff90ff",
                  "a3f1fcaaf638", "4bbc9ef1dcf1", "7aa3354b3911", "99ec19173874","9d275c04c96c","36dcae36116b","33caf0c83b37","06d1de030894",
                  "6e161a868e6e", "f97610f6687b", "f1a3c1e12bc7", "b563a1b54dce","1a01d066c080","6e3331023a99","0a4cff63df55","405f676a0576",
                  "009f670fe134", "bbd3cf536308", "b76f1a7d4b8a", "009eac2d558e","daa7f275c77b","84c482c251b5","ca2e2b33f7d5","69b44c44f3d1",
                  "da35e3a5abba","00a810cfecf0", "ffb6541382aa", "5bb1e17887cf","662fac27db8c","fcd14f4d5b23","8317fcb5b167","a2a2066694de"]

    scrawl_ID = set(start)
    finish_ID = set()

    def start_requests(self):
        while self.scrawl_ID.__len__():
            ID = self.scrawl_ID.pop()
            self.finish_ID.add(ID)


            follows = []
            followsItem = FollowListItem()
            followsItem["_id"] = ID
            followsItem["follows"] = follows


            fans = []
            fansItems = FanListItem()
            fansItems["_id"] = ID
            fansItems["fans"] = fans

            collection = []
            collectionitem = FollowColletionItem()
            collectionitem["_id"] = ID
            collectionitem["collection"] = collection

            likearticle = []
            likearticleitem = LikeArticleItem()
            likearticleitem["_id"] = ID
            likearticleitem["title"] = likearticle


            #构造URL
            # /http://www.jianshu.com/users/7b5031117851/timeline
            url_information = "http://www.jianshu.com/users/%s/timeline" % ID
            url_fans = "http://www.jianshu.com/users/%s/followers" % ID
            url_follow = "http://www.jianshu.com/users/%s/following" % ID
            url_collection = "http://www.jianshu.com/users/%s/subscriptions" % ID
            url_like = "http://www.jianshu.com/users/%s/liked_notes" % ID

            yield Request(url=url_information, meta={"ID":ID}, callback=self.parse0) #爬用户的个人信息
            yield Request(url=url_collection, meta={"item": collectionitem, "result": collection}, callback=self.parse1) #用户的关注专题
            yield Request(url=url_fans, meta={"item": fansItems, "result": fans},callback=self.parse2) #用户的粉丝，目的在于获取ID
            yield Request(url=url_follow, meta={"item":followsItem, "result": follows}, callback=self.parse3) #用户的关注数，目的一是为了获取ID，二是为了获取个人爱好
            yield Request(url=url_like, meta={"item":likearticleitem, "result": likearticle}, callback=self.parse4) #用户的爱好信息，目的是为了获取偏好

    def parse0(self, response):
        #爬取个人的基本信息
        informationItems = InformationItem()
        selector = Selector(response)
        informationItems["_id"] = response.meta["ID"]

        try:
            sexes = selector.xpath(u'//div[@class="title"]/i').extract()
            sex = re.findall('ic-(.*?)">', sexes[0])
            informationItems["sex"] = sex[0]
        except:
            informationItems["sex"] = "未注明"

        try:
            soup = BeautifulSoup(response.text, 'lxml')
            intro = soup.find("div", {"class": "description"}).get_text()
            informationItems["introduction"] = intro
        except:
            informationItems["introduction"] = "暂无简介"

        informationItems["nickname"] = selector.xpath(u'//div[@class="title"]/a/text()').extract()[0]
        informationItems["num_follows"] = selector.xpath('//div[@class="info"]/ul/li[1]/div/a/p/text()').extract()[0]
        informationItems["num_fans"] = selector.xpath('//div[@class="info"]/ul/li[2]/div/a/p/text()').extract()[0]
        informationItems["num_articles"] = selector.xpath('//div[@class="info"]/ul/li[3]/div/a/p/text()').extract()[0]
        informationItems["num_words"] = selector.xpath('//div[@class="info"]/ul/li[4]/div/p/text()').extract()[0]
        informationItems["num_likes"] = selector.xpath('//div[@class="info"]/ul/li[5]/div/p/text()').extract()[0]
        yield informationItems



    #def parse1(self, response):
        #爬取个人所关注的专题
     #   pass


    def parse1(self,response):
        items = response.meta["item"]
        selector = Selector(response)
        total = selector.xpath('//a[@class="title"]').extract()
        if len(total) != 0:
            for one in total:
                c_id = re.findall('href="(.*?)">',one,re.S)
                collection_url = self.host + c_id[0]
                collection = re.findall('>(.*?)<', one, re.S)[0]
                c = collection + collection_url
                response.meta["result"].append(c)
            num = selector.xpath('//li[@class="active"]/a/text()').extract()
            pagenum = re.findall('\d+', num[0], re.S)
            n = pagenum[0]
            if int(n) > 9:
                page = int(n) // 9
                pages = page + 2
                for one in range(1, pages):
                    baseurl = "http://www.jianshu.com/users/%s/subscriptions" % items["_id"]
                    next_url = baseurl + "?page=%s" % one
                    yield Request(url=next_url, meta={"item": items,"result": response.meta["result"]}, callback=self.parse1)
            else:
                yield items
                # 还有一种情况就是已经爬完了第一页，但是没有下一页了response.meta["ID"]
        else:
            e = "没有关注专题"
            response.meta["result"].append(e)
            yield items

    def parse2(self, response):
        items = response.meta["item"]
        #这样做的目的只是为了到时能够返回item,但是实际上我们所操作的是result这个列表
        #爬取粉丝数
        selector = Selector(response)
        total = selector.xpath('//a[@class="name"]').extract()
        #去重，添加ID
        if len(total) != 0:
            for fan in total:
                fan = fan.encode("utf-8")
                ID = re.findall('/u/(.*?)">',fan,re.S)
                a = ID[0]
                if a not in self.finish_ID:
                    self.scrawl_ID.add(a)
                nickname = re.findall('>(.*?)<',fan,re.S)
                response.meta["result"].append(nickname[0])
        #获取更多的ID,翻页

            num = selector.xpath('//li[@class="active"]/a/text()').extract()
            pagenum = re.findall('\d+', num[0], re.S)
            n = pagenum[0]
            if int(n) > 9:
                page = int(n)//9
                pages = page + 2
                if pages < 101:
                    for one in range(1, pages):
                        baseurl = "http://www.jianshu.com/users/%s/followers"%items["_id"]
                        #http://www.jianshu.com/users/deeea9e09cbc/followers?page=4
                        next_url = baseurl + "?page=%s"%one
                        yield Request(url=next_url, meta={"item": items,
                                                          "result": response.meta["result"]}, callback=self.parse2)
                else:
                    for one in range(1,101):
                        baseurl = "http://www.jianshu.com/users/%s/followers" % items["_id"]
                        # http://www.jianshu.com/users/deeea9e09cbc/followers?page=4
                        next_url = baseurl + "?page=%s" % one
                        yield Request(url=next_url, meta={"item": items,
                                                          "result": response.meta["result"]}, callback=self.parse2)

            else:
                yield items
        #还有一种情况就是已经爬完了第一页，但是没有下一页了response.meta["ID"]
        else:
            e = "没有粉丝"
            response.meta["result"].append(e)
            yield items






   # def parse3(self, response):
      #  pass

    def parse3(self, response):
        items = response.meta["item"]
        # 这样做的目的只是为了到时能够返回item,但是实际上我们所操作的是result这个列表
        # 爬取粉丝数
        selector = Selector(response)
        total = selector.xpath('//a[@class="name"]').extract()
        # 去重，添加ID
        if len(total) != 0:
            for follow in total:
                follow = follow.encode("utf-8")
                ID = re.findall('/u/(.*?)">', follow, re.S)
                a = ID[0]
                if a not in self.finish_ID:
                    self.scrawl_ID.add(a)
                nickname = re.findall('>(.*?)<', follow, re.S)
                response.meta["result"].append(nickname[0])
                # 获取更多的ID,翻页

            num = selector.xpath('//li[@class="active"]/a/text()').extract()
            pagenum = re.findall('\d+', num[0], re.S)
            n = pagenum[0]
            if int(n) > 9:
                page = int(n) // 9
                pages = page + 2
                if pages < 101:
                    for one in range(1, pages):
                        baseurl = "http://www.jianshu.com/users/%s/following" % items["_id"]
                        # http://www.jianshu.com/users/deeea9e09cbc/followers?page=4
                        next_url = baseurl + "?page=%s" % one
                        yield Request(url=next_url, meta={"item": items,
                                                      "result": response.meta["result"]}, callback=self.parse3)
                else:
                    for one in range(1,101):
                        baseurl = "http://www.jianshu.com/users/%s/following" % items["_id"]
                        # http://www.jianshu.com/users/deeea9e09cbc/followers?page=4
                        next_url = baseurl + "?page=%s" % one
                        yield Request(url=next_url, meta={"item": items,
                                                          "result": response.meta["result"]}, callback=self.parse3)

            else:
                yield items
        # 还有一种情况就是已经爬完了第一页，但是没有下一页了response.meta["ID"]
        else:
            e = "没有关注"
            response.meta["result"].append(e)
            yield items

    def parse4(self, response):
        items = response.meta["item"]
        selector = Selector(response)
        total = selector.xpath('//a[@class="title"]').extract()
        if len(total) != 0:
            for one in total:
                l_id = re.findall('href="(.*?)">', one, re.S)
                title_url = self.host + l_id[0]
                title = re.findall('>(.*?)<', one, re.S)[0]
                t = title + title_url
                response.meta["result"].append(t)


            num = selector.xpath('//li[@class="active"]/a/text()').extract()
            pagenum = re.findall('\d+', num[0], re.S)
            n = pagenum[0]
            if int(n) > 9:
                page = int(n) // 9
                pages = page + 2
                baseurl = "http://www.jianshu.com/users/%s/liked_notes" % items["_id"]
                for one in range(1, pages):
                    next_url = baseurl + "?page=%s" % one
                    yield Request(url=next_url, meta={"item": items, "result": response.meta["result"]}, callback=self.parse4)
            else:
                yield items
                # 还有一种情况就是已经爬完了第一页，但是没有下一页了response.meta["ID"]
        else:
            e = "没有关注专题"
            response.meta["result"].append(e)
            yield items
