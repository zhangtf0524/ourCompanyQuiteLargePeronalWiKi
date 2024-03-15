# -*- coding: utf-8 -*-
# @Time    : 2024/3/14  13:04
# @FileName: create_db_sql.py
# @Software: vsCode
"""
    Description: 初始化数据库专用，不加载
"""

import sqlite3
import json
conn = sqlite3.connect('/data/personal_wiki/db/personal_wiki.db')
c=conn.cursor()

c.execute('''PRAGMA foreign_keys = ON;''')

c.execute('''
drop table if exists sampleData
''')
c.execute('''
drop table if exists uploadFiles
''')
c.execute('''
drop table if exists wikiZone
''')
c.execute('''
drop table if exists user
''')
c.execute('''
CREATE TABLE "user" (
  "userID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "userName" TEXT NOT NULL,
  "userPassword" TEXT NOT NULL,
  "role" TEXT,
  "status" TEXT NOT NULL,
  "registerTime" text,
  "lastLoginTime" text,
  "mobilePhone" TEXT,
  "createTime" text,
  "modifyTime" text,
  "isDelete" integer,
  "comment" TEXT
);
''')
c.execute('''
CREATE TABLE "wikiZone" (
  "zoneID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "userID" INTEGER NOT NULL,
  "zoneName" TEXT NOT NULL,
  "createTime" text,
  "modifyTime" text,
  "isDelete" integer,
  "comment" TEXT,
  CONSTRAINT "fk_wikiZone_user_1" FOREIGN KEY ("userID") REFERENCES "user" ("userID")
);
''')
c.execute('''
CREATE TABLE if not exists "uploadFiles" (
  "fileID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "zoneID" INTEGER NOT NULL,
  "fileName" TEXT NOT NULL ,
  "fileType" TEXT ,
  "filePosition" TEXT NOT NULL,
  "status" TEXT,
  "fileSize" TEXT ,
  "attributeCode" TEXT,
  "createTime" text,
  "modifyTime" text,
  "isDelete" integer,
  "comment" TEXT,
  CONSTRAINT "fk_uploadFiles_wikiZone_1" FOREIGN KEY ("zoneID") REFERENCES "wikiZone" ("zoneID")
);
''')
c.execute('''
CREATE TABLE "sampleData" (
  "sampleID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "fileID" INTEGER NOT NULL,
  "dataText" TEXT,
  "splitNum" integer,
  "createTime" text,
  "modifyTime" text,
  "isDelete" integer,
  "comment" TEXT,
  CONSTRAINT "fk_processData_uploadFiles_1" FOREIGN KEY ("fileID") REFERENCES "uploadFiles" ("fileID")
);
''')


#c.execute('''delete from user;''')
#c.execute('''insert into user values(null,'name3','password1','admin','1','2024-01-01T00:01:01','2024-01-01T00:01:01','123123123123','2024-01-01T00:01:01','2024-01-01T00:01:01','0','');''')
#c.execute('''insert into wikiZone values(null,4,'zone3','2024-01-01','2024-01-01T00:01:01','1',null)''')
#c.execute('''insert into uploadFiles values(null,4,'file3','txt','1','100kb','md51102931288==','2024-01-01T00:01:01','2024-01-01T00:01:01','0','testfile')''')
#c.execute('''insert into sampleData values(null,5,'abcdefg','2024-01-01T00:01:01','2024-01-01T00:01:01','0',null)''')
#conn.commit()
#c.execute('''select *from sampleData''')
# c.execute('''
# select
# t1.userID,
# t2.zoneID,
# t3.fileID,
# t4.sampleID
# from user t1
# inner join wikiZone t2
# on t1.userID = t2.userID
# inner join uploadFiles t3
# on t2.zoneID = t3.zoneID
# inner join sampleData t4
# on t3.fileID = t4.fileID
# ''')
#sql = f"UPDATE sampleData SET isDelete = 1 WHERE sampleID = 100"
# c.execute(sql)
# conn.commit()
#
# result = c.fetchall()
# for row in result:
#     print (row)

c.close()
conn.close()



