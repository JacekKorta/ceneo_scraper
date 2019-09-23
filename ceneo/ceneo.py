from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


class CeneoPaginationLink:
    page_urls = []
    # sample link: '/Maszyny_do_szycia;0020-30-0-0-10.htm'
    def __init__(self, page_url):
        self.page_url = page_url
        CeneoPaginationLink.page_urls.append(self.page_url)

class Product:
    product_list = []

    def __init__(self, product_code, ceneo_number):
        self.product_code = product_code
        self.ceneo_number = ceneo_number
        Product.product_list.append(self)




def findAllPaginationLinks(url, category):
    html = urlopen('https://www.ceneo.pl{}'.format(url))
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find('div', {'class', 'pagination'}).find_all('a', {'href': re.compile('/'+category+';.*?.htm$')}):
        if 'href' in link.attrs:
            if link.attrs['href'] not in CeneoPaginationLink.page_urls:
                url = link.attrs['href']
                CeneoPaginationLink(url)
                findAllPaginationLinks(url, category)
    return ''


def findAllProducts(url):
    html = urlopen('https://www.ceneo.pl{}'.format(url))
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find('div', {'class', 'page-tab-content'}).find_all('a', {'href': re.compile('^/'+'[0-9]{8}')}):
        if ('href' and 'title') in link.attrs:
            if not ('Dodaj' in link.attrs['title'] or 'Opinie' in link.attrs['title'] or link.attrs['title'] == ''):
                Product(link.attrs['title'], link.attrs['href'][:9])


def getInfoFromProductCard(ceneo_number, product_code):
    offers = []
    html = urlopen('https://www.ceneo.pl{}'.format(ceneo_number))
    bs = BeautifulSoup(html, 'html.parser')
    for offer in bs.find_all('tr'):
        try:
            if ("data-price" and 'data-shopurl') in offer.attrs:
                shop_name = offer['data-shopurl']
                price_info = offer.find('td', {'class', 'cell-price'})
                value = price_info.find('span', {'class', 'value'}).text
                penny = price_info.find('span', {'class', 'penny'}).text
                # offers.append('Sprzedawca: {} cena: {}{}'.format(offer['data-shopurl'], value, penny))
                new_offer = '{};{};{}{}\n'.format(product_code, shop_name, value, penny)
                if new_offer not in offers:
                    offers.append(new_offer)
        except AttributeError:
            print('ups..')
    return offers
