# -*- coding: utf-8 -*-
import requests
from os import path
from os import makedirs
from bs4 import BeautifulSoup as bs4

site = 'http://ptstmn.ru'
site2 = 'http://ptstmn.github.io'
error1 = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8 >'
#Сохранение файла
def SavingFile(file, link = ''):
    if not (file.find('.ru')>0):
        if FileExist(file):
            link = site + '/' + link
            link = requests.get(link)
            FilePath = path.dirname(file)
            if not (FilePath == ''):
                if not (path.exists(FilePath)):
                    makedirs(FilePath)
            url = link.url
            #Картинки
            if url[-3:] == 'png' or url[-3:] == 'jpg' or url[-4:] == 'jpeg' or url[-3:] == 'ico':
                OpenFile = open(file, "wb")
                OpenFile.write(link.content)
                OpenFile.close()
            #JavaScript and CSS
            elif url[-2:] == 'js' or url[-3:] == 'css':
                r = requests.get(url)
                with open(file, "wb") as code:
                    code.write(r.content)
            #Остальное в частности HTML
            else:
                OpenFile = open(file, 'w', encoding='utf8')
                text = link.text
                text = text.replace(site, site2)
                text = text.replace(error1, '')
                with OpenFile:
                    for char in text:
                        OpenFile.write(char)
                OpenFile.close()
            return True
        else:
            return False
    else:
        return False

#Поиск ссылок на сохраненной странице
def FindHref(file):
    OpenFile = open(file, 'r', encoding='utf8')
    CurrentPage = bs4(OpenFile, "html5lib")
    OpenFile.close()
    a = CurrentPage.find_all('a')
    se = set()
    for i in a:
        try:
            href = i.attrs['href']
            if href.find( 'html' ) > 0:
                flag = True
            else:
                flag = False
            if flag:
                se.add(href)
        except KeyError:
            pass
    return se

#Поиск картинок
def FindPict(file):
    OpenFile = open(file, 'r', encoding='utf8')
    CurrentPage = bs4(OpenFile, "html5lib")
    OpenFile.close()
    pict = CurrentPage.find_all('img')
    se = set()
    for i in pict:
        try:
            href = i.attrs['src']
            se.add(href)
        except KeyError:
            pass
    return se

#Поиск картинок в CSS
def FindPictInCSS(file):
    OpenFile = open(file, 'r', encoding='utf8')
    se = set()
    for i in OpenFile.readlines():
        if i.find('url')>-1:
            url = i[i.find('url')+6:i.find(')',i.find('url'))]
            se.add(url)
    OpenFile.close()
    return se

#Поиск JavaScrypt
def FindJS(file):
    OpenFile = open(file, 'r', encoding='utf8')
    CurrentPage = bs4(OpenFile, "html5lib")
    OpenFile.close()
    pict = CurrentPage.find_all('script', attrs={'type' : 'text/javascript'})
    se = set()
    for i in pict:
        try:
            href = i.attrs['src']
            se.add(href)
        except KeyError:
            pass
    return se

#Поиск CSS
def FindCSS(file):
    OpenFile = open(file, 'r', encoding='utf8')
    CurrentPage = bs4(OpenFile, "html5lib")
    OpenFile.close()
    pict = CurrentPage.find_all('link', attrs={'type' : 'text/css'})
    se = set()
    for i in pict:
        try:
            href = i.attrs['href']
            se.add(href)
        except KeyError:
            pass
    return se

#Поиск ICO
def FindICO(file):
    OpenFile = open(file, 'r', encoding='utf8')
    CurrentPage = bs4(OpenFile, "html5lib")
    OpenFile.close()
    pict = CurrentPage.find_all('link', attrs={'type' : 'image/x-icon'})
    se = set()
    for i in pict:
        try:
            href = i.attrs['href']
            se.add(href)
        except KeyError:
            pass
    return se

#Проверка существования файла
def FileExist(file):
    return(not(path.exists(file)))

def SaveCSS(whatt = set()):
    while whatt.__len__()>0:
        j = whatt.pop()
        if j[:1]=='/':
            j = j[1:]
        SavingFile(j, j)
        PIC = FindPictInCSS(j)
        while PIC.__len__()>0:
            pic = PIC.pop()
            if pic[:1]=='/':
                pic = pic[1:]
            SavingFile(pic, pic)

def SaveICO(whatt = set()):
    while whatt.__len__()>0:
        j = whatt.pop()
        if j[:1]=='/':
            j = j[1:]
        SavingFile(j, j)

def SavePict(whatt = set()):
    while whatt.__len__()>0:
        j = whatt.pop()
        if j[:1]=='/':
            j = j[1:]
        SavingFile(j, j)

def SaveJS(whatt = set()):
    while whatt.__len__()>0:
        j = whatt.pop()
        if j[:1]=='/':
            j = j[1:]
        SavingFile(j, j)

SavingFile('index.html')
links = FindHref('index.html')
while links.__len__()>0:
    i = links.pop()
    if i[:1]=='/':
        i = i[1:]
    if SavingFile(i, i):
        whatt = FindHref(i)
        links = links|whatt
        #Pict
        whatt = FindPict(i)
        SavePict(whatt)
        #JS
        whatt = FindJS(i)
        SaveJS(whatt)
        #CSS
        whatt = FindCSS(i)
        SaveCSS(whatt)
        #ICO
        whatt = FindICO(i)
        SaveICO(whatt)