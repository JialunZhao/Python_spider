#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-16 18:10:04
# @Author  : 赵佳仑 (jialun_zhao@hotmail.com)
# @Link    : https://github.com/JialunZhao
# @Version : $v1.0$

import os
import pymysql
import requests
import time
import urllib.request
from bs4 import BeautifulSoup
import codecs
import re

##################################################
# pymysql.Connect()参数说明
# host(str):      MySQL服务器地址
# port(int):      MySQL服务器端口号
# user(str):      用户名
# passwd(str):    密码
# db(str):        数据库名称
# charset(str):   连接编码

# connection对象支持的方法
# cursor()        使用该连接创建并返回游标
# commit()        提交当前事务
# rollback()      回滚当前事务
# close()         关闭连接

# cursor对象支持的方法
# execute(op)     执行一个数据库的查询命令
# fetchone()      取得结果集的下一行
# fetchmany(size) 获取结果集的下几行
# fetchall()      获取结果集中的所有行
# rowcount()      返回数据条数或影响行数
# close()         关闭游标对象
##################################################
##################################################
# 简单爬虫框架：
#　　爬虫调度器 -> URL管理器 -> 网页下载器(urllib2) -> 网页解析器(BeautifulSoup) -> 价值数据
##################################################

# 连接数据库
DB = pymysql.Connect(
    # host = 'localhost',
    # port = 3306,
    user='root',
    # passwd = 'XYZz19890401',
    db='python',
    charset='utf8'
)

# 获取游标
cursor = DB.cursor()

# 目标页面链接获取函数


def get_url(host_url, url_index):
    # 爬虫抓取部分
    headers = {'User-Agent': 'Mozilla/5.0',
               "Content-Type": "text/html; charset=gb2312"}
    response = requests.post(host_url, headers=headers)
    # 使用headers避免访问受限
    soup = BeautifulSoup(response.content.decode('gbk'), 'html.parser')
    items = soup.find_all('a')
    host_title = str(soup.title.string)
    # print(soup.prettify())
    # print(items)
    # print(title)

    # 爬取URL信息
    url = ''
    url_tmp = ''
    for index, item in enumerate(items):
        if item:
            if item.get('href') is not None and item.get('title') is not None and item.get('class') is None:
                url_tmp = item.get('href')
                if url_tmp != url:
                    url = url_tmp
                    title = item.get('title')
                    # print(title)
                    # print(url)

                    # SQL 插入语句
                    sql = "INSERT INTO t_url_download(host_title, host_url,title, url, url_num) VALUES ('%s', '%s', '%s', '%s', '%d')" \
                        % (host_title, host_url, title, 'https:' + url, url_index)
                    try:
                        # 执行sql语句
                        cursor.execute(sql)
                        # 执行sql语句
                        DB.commit()
                    except:
                        # 发生错误时回滚
                        DB.rollback()
                    url_index = url_index + 1
    return url_index

# 爬取图片链接并下载


def get_img(url_id, host_title, host_url):
    # 爬虫抓取部分
    # host_url = 'https://club.autohome.com.cn/bbs/thread/bff2084b0b6f339d/10457106-1.html'
    headers = {'User-Agent': 'Mozilla/5.0',
               "Content-Type": "text/html; charset=gb2312"}
    response = requests.post(host_url, headers=headers)
    # 使用headers避免访问受限
    # print(response.content)
    soup = BeautifulSoup(response.content.decode(
        'gbk', 'ignore'), 'html.parser')
    items = soup.find_all('img')
    title = str(soup.title.string)

    # 文件保存位置配置
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    title = re.sub(rstr, "_", title)  # 替换为下划线
    folder_path = './Downloader-autohome/'+title+'/'
    if os.path.exists(folder_path) == False:  # 判断文件夹是否已经存在
        os.makedirs(folder_path)  # 创建文件夹

    # print(soup.prettify())
    print(title)
    # 爬取图片信息
    img_index = 0
    for index, item in enumerate(items):
        if item:
            if item.get('src9') is None:
                img_url = item.get('src')
            else:
                img_url = item.get('src9')
                # get函数获取图片链接地址，requests发送访问请求
            if img_url is None:
                img_url = 'img_url is None'
            else:
                img_url = 'https:' + img_url
            if re.match(r"(.*)album(.*)", img_url):
                img_index = img_index + 1
                # print(img_url)
                img_url = img_url.replace('500_', '')
                response = requests.get(img_url)
                img_name = folder_path + str(img_index) + '.jpg'
                # print(img_url)
                with open(img_name, 'wb') as img:
                    img.write(response.content)
                    img.close()
                # print('第%d张图片下载完成' % (img_index))
                time.sleep(0.1)  # 自定义延时
                # SQL 插入语句
                sql = "INSERT INTO t_img_download(url_id, host_title, host_url , img_web_title,img_url,img_num) VALUES ('%d','%s', '%s','%s', '%s', '%d')" \
                    % (url_id, host_title, host_url, title, img_url, img_index)
                # print(sql)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 执行sql语句
                    DB.commit()
                except:
                    # 发生错误时回滚
                    DB.rollback()
    sql = "UPDATE t_url_download SET state_flag = 1 WHERE ID = '%d'"
    data = url_id
    try:
        # 执行sql语句
        cursor.execute(sql % data)
        # 执行sql语句
        DB.commit()
    except:
        # 发生错误时回滚
        DB.rollback()
    return img_index


# 准备URL
web_url = 'https://club.autohome.com.cn/jingxuan/292/'
url_index = 1
url_page = 1
while url_page < 14:
    url_link = web_url + str(url_page)
    url_page += 1
    print(url_link)
    # url_index = get_url(url_link, url_index)
    # time.sleep(1)  # 自定义延时


# 读取数据
sql = 'SELECT *  FROM t_url_download where state_flag = 0  LIMIT 100 '
# print(sql)
cursor.execute(sql)
img_num = 0
page_num = cursor.rowcount
# 下载开始
for rows in cursor.fetchall():
    print(rows)
    img_num = img_num + get_img(rows[0], rows[3], rows[4])
    time.sleep(0.5)  # 自定义延时

print(page_num, '页已下载完成 ， 共下载图片 ', img_num, ' 张')


# # # 关闭数据库连接
DB.close()
