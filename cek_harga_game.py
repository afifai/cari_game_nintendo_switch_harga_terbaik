import requests
from bs4 import BeautifulSoup

def harga_to_float(harga):
    if ' ' in harga:
        harga = harga.split()[-1]
    harga = harga[2:]
    harga = harga.replace('.','')
    harga = harga.replace(',','.')
    return eval(harga)

query = input("Masukkan game yang Anda cari : ")
url = 'https://eshop-prices.com/games?currency=IDR&q={}'.format(query)
headers = {
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
data = requests.get(url, headers=headers)
if data.status_code == 200:
    soup = BeautifulSoup(data.text, 'html.parser')
    lists = soup.find_all('a', class_='games-list-item')
    out = "HASIL PENCARIAN : \n"
    links = {}
    i = 1
    for item in lists:
        judul_game = item.find('h5').text.strip()
        harga = item.find('span', class_='price-tag').text.strip()
        link = 'https://eshop-prices.com'+item['href']
        links[i] = link
        out += '{}. {} ({})\n'.format(i, judul_game, harga)
        i += 1
    print(out)
else:
    print("Pencarian gagal, silahkan coba lagi")

if links != {}:
    pilihan = input("Masukkan angka pilihan Anda : ")
    pilihan = int(pilihan)
    if pilihan in links.keys():
        url = links[pilihan]
        data = requests.get(url, headers=headers)
        if data.status_code == 200:
            soup = BeautifulSoup(data.text, 'html.parser')
            judul_game = soup.find('h1').text.strip()
            lists = soup.find_all('tr', class_='pointer')
            regions = {}
            for item in lists:
                d = item.find_all('td')
                negara = d[1].text.strip()
                harga = d[3].text.strip()
                harga = harga_to_float(harga)
                regions[negara] = harga
            out = "HARGA TERBAIK DARI GAME {}\n".format(judul_game)
            for key, value in tuple(regions.items())[:5]:
                out += 'Region {} : Rp{:,.2f}\n'.format(key, value)
            print(out)
        else:
            print("Pengambilan detail Game gagal")
