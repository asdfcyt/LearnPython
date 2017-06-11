# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultercoding('utf-8')
import MySQLdb


class Mysql():
    #绑定3个基本的参数，表名，字段列表，字段数量

    def __init__(self, table_name, field_list=[], field_num=0):
        self.table_name = table_name
        self.field_list = field_list
        self.field_num = field_num

    def create_table(self):
        Field_list = []
        for field in self.field_list:
            field += 'varchar(500)'
            Field_list.append(field)
        field_str = '.'.join(Field_list)
        engine = 'engine=innodb default charset=utf8'
        create_sql_str = 'create table IF NOT EXISTS %s(%s)%s' %(self.table_name, field_str, engine)
        print create_sql_str
        conn = MySQLdb.connect(host='localhost', user='root', passwd="882645", db='local_db', port=3306, charset='utf8')
        with conn:
            cursor = conn.cursor()
            cursor.execute(create_sql_str)


    def insert(self, item={}):
        conn = MySQLdb.connect(host='localhost', user='root', passwd="882645", db='local_db', port=3306, charset='utf8')

        #列表转字符串，用于构造insert_sql
        data = '.'.join(["'" + item[i] + "'" for i in range(1, self.field_num+1)])
        with conn:
            cursor = conn.cursor()
            insert_sql = 'inser into %s value(%s)' % (self.table_name, data)
            print insert_sql
            cursor.execute(insert_sql)
            conn.commit()

