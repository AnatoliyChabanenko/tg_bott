import json
import requests
from bs4 import BeautifulSoup as BS


class Nibulon:
    URL = 'https://nibulon.com/data/zakupivlya-silgospprodukcii/zakupivelni-cini.html'
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
        'accept': '*/*'}
    
    def get_content(self ,params=None):
        r = requests.get(self.URL, headers=self.HEADERS, params=params)
        name = []
        price = []
        soup = BS(r.text, 'html.parser')
        for i in soup.find('div' , class_ = 'card mt-3').find_all('div', class_='culture_item'):
            prise = (i.a.strong.text.strip())
            name.append(i.a.text.replace(prise, '').strip("\n\r- "))
            price.append(prise.replace('грн/т', ''))
        return dict(zip(name, price))

    def update_content(self):
        data = self.get_content(self.URL)
        with open('data1.json', 'w') as f:
            print(data)
            json.dump(data, f)

if __name__ == '__main__':
    data = Nibulon()
    data.update_content()
