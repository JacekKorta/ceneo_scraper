from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


class CeneoPaginationLink:
    page_urls = []

    def __init__(self, page_url):
        self.page_url = page_url
        CeneoPaginationLink.page_urls.append(self.page_url)


def findAllPaginationLinks(new_url, category):
    html = urlopen('https://www.ceneo.pl{}'.format(new_url))
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find('div', {'class', 'pagination'}).find_all('a', {'href': re.compile('/'+category+';.*?.htm$')}):
        if 'href' in link.attrs:
            if link.attrs['href'] not in CeneoPaginationLink.page_urls:
                print(CeneoPaginationLink.page_urls)
                new_url = link.attrs['href']
                print(new_url)
                CeneoPaginationLink(new_url)
                findAllPaginationLinks(new_url, category)
    return ''


