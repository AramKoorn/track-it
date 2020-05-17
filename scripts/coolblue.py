from bs4 import BeautifulSoup
from requests import get
from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime
import requests
from bs4.dammit import EncodingDetector
import re
import json


class FindSwitch(ABC):
    def __init__(self, url):
        self.url = url

    def scrape(self, url):
        response = get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def get_date(self):
        return datetime.now()

    @abstractmethod
    def evaluate(self):
        pass


class CoolBLue(FindSwitch):
    def __init__(self):
        pass

    def get_url(self):
        resp = requests.get("https://www.coolblue.nl/consoles/nintendo-switch")
        http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
        encoding = html_encoding or http_encoding
        soup = BeautifulSoup(resp.content, from_encoding=encoding)

        list_href = []
        for link in soup.find_all('a', href=True):
            if 'nintendo-switch-2019-upgrade-' in link['href']:
                list_href.append(link['href'])
        return set(list_href)

    def get_product_information(self, soup):
        """
        Gets the script tag where all the product information is and stores it as a python dictionary.

        :param soup: Beautifulsoup instance
        :return: Dictionary containing the product information
        """

        script_tags = []
        # Todo make this faster
        for script in soup(text=re.compile(r'ecomm_pvalue')):
            script_tags.append(script.parent)

        json_text = '{%s}' % (str(script_tags[0]).partition('{')[2].rpartition('}')[0],)
        dict_info = json.loads(json_text)
        dict_info = dict_info['google_tag_params']

        return dict_info

    def evaluate(self):

        urls = self.get_url()
        df = pd.DataFrame()

        for url in urls:

            url = 'https://www.coolblue.nl/' + url
            html_soup = self.scrape(url)
            product_info = self.get_product_information(html_soup)
            dict_tmp = {}
            dict_tmp['product_name'] = [url.split('/')[6].replace('.html', '')]
            dict_tmp['state'] = product_info['ecomm_availability']
            dict_tmp['price'] = product_info['ecomm_pvalue']
            dict_tmp['left_in_stock'] = product_info['ecomm_quantity']
            dict_tmp['product_id'] = product_info['ecomm_prodid']
            dict_tmp['last_refreshed'] = [self.get_date().strftime("%Y-%m-%d %H:%M:%S")]


            df = pd.concat([df, pd.DataFrame.from_dict(dict_tmp)])
            del dict_tmp

        return df


def run():

    df = CoolBLue().evaluate()

    # for script in html_soup(text=re.compile(r'ecomm_pvalue')):
    #     print(script.parent)

    pass


if __name__ == '__main__':
   run()









