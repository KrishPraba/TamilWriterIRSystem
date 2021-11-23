#Installing Libraries

import requests
from bs4 import BeautifulSoup
import wikipedia
import json
import pandas as pd


#Functions needed for scraping

def getWriterList():
    response = requests.get(url="https://ta.wikipedia.org/wiki/%E0%AE%A4%E0%AE%AE%E0%AE%BF%E0%AE%B4%E0%AF%8D_%E0%AE%8E%E0%AE%B4%E0%AF%81%E0%AE%A4%E0%AF%8D%E0%AE%A4%E0%AE%BE%E0%AE%B3%E0%AE%B0%E0%AF%8D%E0%AE%95%E0%AE%B3%E0%AF%8D_%E0%AE%AA%E0%AE%9F%E0%AF%8D%E0%AE%9F%E0%AE%BF%E0%AE%AF%E0%AE%B2%E0%AF%8D")
    soup = BeautifulSoup(response.content, 'html.parser')
    writers1 = []
    titles = soup.find_all('li', class_=False)
    for title in titles:
        t = title.find('a')
        if t is not None:
            if t.string is not None:
                writers1.append(t.string.strip())
    del writers1[-10:]
    
    response = requests.get(url="https://ta.wikipedia.org/wiki/%E0%AE%AA%E0%AE%95%E0%AF%81%E0%AE%AA%E0%AF%8D%E0%AE%AA%E0%AF%81:%E0%AE%A4%E0%AE%AE%E0%AE%BF%E0%AE%B4%E0%AF%8D_%E0%AE%8E%E0%AE%B4%E0%AF%81%E0%AE%A4%E0%AF%8D%E0%AE%A4%E0%AE%BE%E0%AE%B3%E0%AE%B0%E0%AF%8D%E0%AE%95%E0%AE%B3%E0%AF%8D")

    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find_all('div', class_='mw-category-group')
    writers2 = []
    for d in div:
        titles = d.find_all('li')
        for title in titles:
            new = title.find('a').string.strip()
            writers2.append(new)
    writers2 = writers2[12:]

    writers = writers1 + writers2
    writers = list(set(writers))

    writers.index('கல்கி')
    writers.remove('கல்கி')
    writers.append('கல்கி (எழுத்தாளர்)')

    return writers

df = pd.read_excel("books_synonym.txt")
df.info()

book_list = df['books'].tolist()

def find_body_information(url):
    keys = []
    info_dict = {}  
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', class_='mw-parser-output')

    info = div.find('table', class_='infobox biography vcard')

    if info is not None:
        rows = info.find_all('tr')

        for r in rows:
            head = r.find('th')
            col = r.find('td')
            if ((col is not None) and (head is not None) and (head.string is not None)):
                keys.append(head.string.strip())
                info_dict[head.string.strip()] = ' '.join(col.find_all(string=True))
    
        for book in book_list:
            sub_head = div.find('span',class_='mw-headline',string=book)
            if sub_head is not None:
                if sub_head.find_next('ol') is not None:
                    books = sub_head.find_next('ol')
                    b = books.find_all(string=True)
                elif sub_head.find_next('ul') is not None:
                    books = sub_head.find_next('ul')
                    b = books.find_all(string=True)
                
                if b is not None:
                    boos = []
                    for boo in b:
                        boos.append(boo.strip())
                    info_dict['எழுதிய நூல்கள்'] = boos
                    keys.append('எழுதிய நூல்கள்')
                    break
    return [keys,info_dict]


final_keys = ['இறப்பு', 'தேசியம்', 'பிறப்பு', 'எழுதிய நூல்கள்', 'பட்டம்', 'இருப்பிடம்', 'அறியப்படுவது','முக்கிய வார்த்தைகள்','தகவல்','சுருக்கம்','பெயர்']

def extract_data(ny):
    data = {}
        
    data['முக்கிய வார்த்தைகள்'] = ny.categories
    data['தகவல்'] = ny.content
    data['சுருக்கம்'] = ny.summary
    data['பெயர்'] = ny.title
    information = find_body_information(ny.url)
    heading_titles = information[0]
    data.update(information[1])

    return [data,heading_titles]

def data_scraper(writers):
    wikipedia.set_lang("ta")
    result = []
    total_keys = []

    for writer in writers:
        try:
            ny = wikipedia.page(writer)
            output = extract_data(ny)
            result.append(output[0])
            total_keys.append(output[1])

        except wikipedia.DisambiguationError as e:
            print(e.options)

    return result



output = []

famous_writers = getWriterList()
scraped_data = data_scraper(famous_writers)

for r in scraped_data:    
    for k in final_keys:
        if k not in r.keys():
            r[k] = None

    for ke in list(r.keys()):
        if ke not in final_keys:
            del r[ke]
    output.append(r)

#save data

with open('famous_writer_raw.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)