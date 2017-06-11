# encoding=utf-8
import pymongo
from items import InformationItem, FanListItem,FollowColletionItem, LikeArticleItem, FollowListItem


class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["jianshu"]
        self.Information = db["Information"]
        self.FollowColletion = db["FollowColletion"]
        self.LikeArticle = db["LikeArticle"]
        self.Fans = db["Fans"]
        self.FollowList = db["FollowList"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, InformationItem):
            try:
                self.Information.insert(dict(item))
            except Exception:
                pass

        elif isinstance(item, FanListItem):
            fansItems = dict(item)
            try:
                self.Fans.insert(fansItems)
            except Exception:
                pass

        elif isinstance(item, FollowColletionItem):
            try:
                self.FollowColletion.insert(dict(item))
            except Exception:
                pass

        elif isinstance(item, LikeArticleItem):
            try:
                self.LikeArticle.insert(dict(item))
            except Exception:
                pass

        elif isinstance(item, FollowListItem):
            try:
                self.FollowList.insert(dict(item))
            except Exception:
                pass

        return item