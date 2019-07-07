#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : getTuchongSelenium.py
# @Author: Laomaizi
# @email : navyjt@163.com
# @Date  : 2019/7/7
# @Desc  : 通过Selenium插件的方法来捕捉动态渲染页面(需要作者将作品同步至album相册，若作者只是上次到主页，改方法无效)

from selenium import webdriver
import re
import requests
from bs4 import BeautifulSoup
import os

def getFollowing(file):
    followlists = []
    with open(file,'r') as f:
        while True:
            a = f.readline().strip();
            if a:
                followlist = 'https://{}.tuchong.com/albums/'.format(a)
                followlists.append(followlist)
            else:
                break
    return followlists

# 返回https://victorliu.tuchong.com/albums/598343/  这样的url
def getAlbumlist(url):
    albumurl = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                             ' AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/74.0.3729.169 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text

    soup = BeautifulSoup(html,'lxml')
    for i in (soup.select('.albums')):
        albumurl.append(i['href'])
    return albumurl

def getPicFromAlbumUrl(albumurl,artist):
    browser = webdriver.Chrome()
    browser.get(albumurl)
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    html = browser.page_source
    # print(html)
    # return html
    oriurl = 'https://'+ artist+'.tuchong.com/albums/.*?/.*?/'
    regex = re.compile(oriurl)
    items = re.findall(regex,html)
    if len(items):
        for item in items:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                                     ' AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/74.0.3729.169 Safari/537.36'}
            response = requests.get(item, headers=headers)
            response.encoding = 'utf-8'
            html = response.text
            jpgurl = re.findall(r'https://.*?.jpg', html)[0]
            picname = jpgurl.split('/')[-1]
            print(jpgurl)
            dir = artist
            if not os.path.isdir(dir):
                os.mkdir(dir)
            try:
                pic = requests.get(jpgurl, headers=headers)
                if pic.status_code == 200:
                    with open(dir + '/' + picname, 'wb') as fp:
                        fp.write(pic.content)
                        fp.close()
                print("下载完成")
            except Exception as e:
                print('下载出错')


if __name__ == '__main__':
    followlists = getFollowing('followlist.txt')
    for url in followlists:
        artist = re.findall('https://(.*?).tuchong.com/',url)[0]
        albumurl = getAlbumlist(url)
        for onealbum in albumurl:
            getPicFromAlbumUrl(onealbum,artist)
