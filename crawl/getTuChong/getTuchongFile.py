#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : getTuchongFile.py
# @Author: Laomaizi
# @email : navyjt@163.com
# @Date  : 2019/7/4
# @Desc  : 从文件中获取图虫作者的id，爬下相册全部文件

import requests
from bs4 import BeautifulSoup
import re
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

def getAlbumlist(url):
    albumurl = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                             ' AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/74.0.3729.169 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text

    soup = BeautifulSoup(html,'lxml')
    # print(soup)
    for i in (soup.select('.albums')):
        albumurl.append(i['href'])
    return albumurl

# 从https://victorliu.tuchong.com/albums/410883/这样的网址获取ajax地址
# https: // victorliu.tuchong.com / rest / 2 / albums / 410883 / images?count = 12 & page = 3
def getJsonFromOneAlbum(onealbum,artist):
    ajaxurl = onealbum.replace('.com/','.com/rest/2/')
    for i in range(1,3):

        addedurl  = ajaxurl + 'images?count=12&page=' + str(i)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/74.0.3729.169 Safari/537.36'}
        response = requests.get(addedurl, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            parse_json(response.json(),artist)


def parse_json(json,artist):
    if json:
        items = json.get('data').get('image_list')
        if len(items):
            for item in items:
                picurl = item.get('url')
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                                         ' AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/74.0.3729.169 Safari/537.36'}
                response = requests.get(picurl, headers=headers)
                response.encoding = 'utf-8'
                html = response.text
                jpgurl = re.findall(r'https://.*?.jpg',html)[0]
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
            json = getJsonFromOneAlbum(onealbum,artist)
            # parse_json(artist,json)


