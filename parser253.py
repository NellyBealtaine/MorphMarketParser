# -*- coding: utf-8 -*-
"""parser253.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YC4eN_9szg425in6xvj7qTW0SmCN2cdV

## Используя полученные знания о способах сбора данных соберите самостоятельно датасет на 5000 записей с не менее чем 10 переменными
(количественными и категориальными) на любую тему. Сохраните его в виде csv-файла. Сделайте описание датасета (можно в виде Google документа).
В описание дайте краткую характеристику собранных величин и предложите потенциальные сферы применения собранного датасета. Ответ пришлите
в виде ссылки на папку в Google Диске, где будет храниться csv-файл и его описание.
"""

import pandas as pd
import requests
import bs4
import time

page = 1
names = []
hrefs = []
birth = []
maturity = []
weight = []
price = []
store = []
quantity = []

cookies = {
    'JSESSIONID': 'f80673670d429faa',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=f80673670d429faa',
    'Origin': 'https://www.morphmarket.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'content-type': 'text/plain',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

while page<=100:
  r = requests.get('https://www.morphmarket.com/eu/c/all?cat=2&sex=&maturity=0&min_weight=0&max_weight=1000000&prey_state=0&prey_food=0&min_genes=0&max_genes=9&traits=&neg_traits=&min_price=0&max_price=1000000&cur=EUR&epoch=22&store=&nearby_location=&lat=&lng=&radius=&country=&export=&sort=def&layout=list&page='+str(page), headers=headers)
  BS = bs4.BeautifulSoup(r.text) #создаем объект, где будет информация с сайта
  for i in BS.find_all('tr', {'class': ['list-row dzone ', 'list-row dzone on-hold-row']}):
    hrefs.append('https://www.morphmarket.com' + i.get('data-href'))  
  for i in BS.find_all('td', {'class': 'title'}):
    names.append(i.text.replace('\n', '') )
  for i in BS.find_all('td', {'class': 'weight'}):
    weight.append(i.text.replace('\n', '') )
  for i in BS.find_all('td', {'class': 'maturity'}):
    maturity.append(i.text.replace('\n', '') )
  for i in BS.find_all('td', {'class': 'dob'}):
    birth.append(i.text.replace('\n', '') )
  for i in BS.find_all('td', {'class': 'store'}):
    store.append(i.text.replace('\n', '') )
  for i in BS.find_all('td', {'class': 'price'}):
    price.append(i.text.replace('\n', '') )
  for i in BS.find_all('td', {'class': 'quantity'}):
    quantity.append(i.text.replace('\n', '') )
  page += 1

traits = []
traits_item = []
sex = []

for j in range(len(hrefs)):
  item_href = hrefs[j]
  r = requests.get(item_href)
  soup1 = bs4.BeautifulSoup(r.text)
  for k in soup1.find_all('span', {'class': ['badge trait het-rec', 'badge trait dom-codom', 'badge trait pos-rec', 'badge trait vis-rec']}):
    traits_item.append(k.text.replace('\n', '').replace('\t', '') )
  traits.append(traits_item)
  traits_item = []
  s = soup1.find(['i', 'span'], {'alt': ['female', 'male', 'unknown sex']})
  sex.append(s.get('alt'))
  j = j + 1
  time.sleep(5)

for i in range(len(price)):
  if '€' in price[i]:
    price[i] = price[i][price[i].find('€'):-1].strip()
  elif '£' in price[i]:
    price[i] = price[i][price[i].find('£'):-1].strip()
  elif '$' in price[i]:
    price[i] = price[i][price[i].find('$'):-1].strip()
  else:
    price[i] = 0

d = {'Наименование': names, 'Ссылка': hrefs, 'Пол': sex, 'Вес': weight, 'Год рождения': birth, 'Возрастная группа': maturity, 'Продавец': store, 'Стоимость': price, 'Количество': quantity, 'Гены': traits}
df = pd.DataFrame(data = d)
df

df.to_csv('MorphMarketPythons.csv', index=False)