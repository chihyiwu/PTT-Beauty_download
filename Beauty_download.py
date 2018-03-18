import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import os
import sys

def download_images(articles):            
    for article in articles:
        #表特標題資料夾如未建立，則創建資料夾
        if not os.path.isdir(os.path.join('download',article.text)):
            os.mkdir(os.path.join('download',article.text))
        #取得標題連結
        res = requests.get('https://www.ptt.cc'+article['href'])
        #過濾文章內所有圖檔連結
        images = reg_imgur_file.findall(res.text)

        total = len(images)
        count = 0
        if total >0:
            print ("即將開始下載 "+article.text+"，共"+str(total)+"張圖片!")
            for image in set(images):
             #利用re套件搜尋符合正規表示式條件圖檔的，並返回相符的第一個字串內容
             ID = re.search('http[s]?://[i.]*imgur.com/(\w+\.(?:jpg|png|gif))',image).group(1)
             #利用urllib模組，使用裡面的urlretrieve函式庫，將圖片存入對應資料夾
             urlretrieve(image,os.path.join('download',article.text,ID))
             count += 1
             #print ("已經下載: " + str(round(200 * count / total ,2)) + " %.")
             print ("已經下載: " +str(count)+"/"+str(total)+"張。")
                        
            print ("標題： "+article.text+"已下載完畢"+",共抓取"+str(total)+"張圖，請查看資料夾！")
            
def crawler(pages=3):
    #download資料夾,如未存在則建立
    if not os.path.isdir('download'):
        os.mkdir('download')
    #PTT表特版網頁連結    
    url = 'https://www.ptt.cc/bbs/Beauty/index.html'
            
    for round in range(pages):
        #利用requests套件模組取得網頁資料
        res = requests.get(url)
        #利用BeautifulSoup套件模組分析網頁資料的HTML語法
        soup = BeautifulSoup(res.text,'html.parser')
        #表特標題+連結
        articles = soup.select('div.title a')
        #上一頁
        paging = soup.select('div.btn-group-paging a')
        #往上一頁網址
        next_url = 'https://www.ptt.cc'+paging[1]['href']
        url = next_url
        download_images(articles)
        
#符合正規表示式條件的圖檔，可自動過濾符合條件
reg_imgur_file = re.compile('http[s]?://[i.]*imgur.com/\w+\.(?:jpg|png|gif)')
crawler(int(sys.argv[1]))
