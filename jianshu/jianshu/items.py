# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InformationItem(scrapy.Item):
    #个人信息
    _id = scrapy.Field()
    nickname = scrapy.Field()
    sex = scrapy.Field()
    num_follows = scrapy.Field()
    num_fans = scrapy.Field()
    num_articles = scrapy.Field()
    num_words = scrapy.Field()
    num_likes = scrapy.Field()
    introduction = scrapy.Field()

class FollowColletionItem(scrapy.Item):
    #关注的专题
    _id = scrapy.Field()
    #nickname = scrapy.Field()
    collection = scrapy.Field()
    #collection_url = scrapy.Field()

class LikeArticleItem(scrapy.Item):
    _id = scrapy.Field()
    #nickname = scrapy.Field()
    title = scrapy.Field()
    #title_url = scrapy.Field()

class FanListItem(scrapy.Item):
    _id = scrapy.Field()
    #nickname = scrapy.Field()
    fans = scrapy.Field()

class FollowListItem(scrapy.Item):
    _id = scrapy.Field()
    #nickname = scrapy.Field()
    follows = scrapy.Field()
    #user_url = scrapy.Field()







