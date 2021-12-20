import requests
from lxml import etree
from typing import Callable, Any
import urllib
import os
from config import config


DOWNLOAD_PATH = config.download_path

# Interfaces, reader returns a HTML
# parser parse the HTML, return result
Reader = Callable[[Any], etree.HTML]
Parser = Callable[[etree.HTML], Any]

### Reader
def get_request(url:str) -> etree.HTML:
    """Simple request"""
    html = requests.get(url).content.decode('utf-8')
    html = etree.HTML(html)
    return html

def request_wiki(keyword:str) -> etree.HTML:
    """Request by keyword"""
    url = f"https://en.wikipedia.org/wiki/{keyword}"
    return get_request(url)

### Parser
def parse_article(html:etree.HTML) -> str:
    """Extract texts from articles"""
    return ''.join(html.xpath('//div[@id="bodyContent"]//text()'))

def parse_link(html:etree.HTML, base_url:str = "https://en.wikipedia.org/") -> dict:
    """Extract links from an article"""
    words = html.xpath('//div[@id="bodyContent"]//a/text()')
    urls = html.xpath('//div[@id="bodyContent"]//a/@href')
    result = dict(zip(words, urls))
    result = {k: urllib.parse.urljoin(base_url, v) 
            for k, v in result.items() 
            if v.startswith('/wiki')}
    return result


class WikiDownloader:
    def __init__(self, keyword, num_articles = 50, base_path = DOWNLOAD_PATH):
        self.keyword = keyword
        self.links = {}
        self.visited = []
        self.keyword_path = os.path.join(base_path, f"{keyword}")
        if not os.path.exists(self.keyword_path):
            os.makedirs(self.keyword_path)
        self.num_articles = num_articles
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        

    def start_request(self):
        """Start from a keyword request"""
        html = request_wiki(self.keyword)
        return parse_link(html)

    def download_articles(self):
        """Follow links of the keyword page."""
        for keyword, link in self.start_request().items():

            if len(self.visited) > self.num_articles:
                break

            try:
                if keyword not in self.visited:
                    html = get_request(link)
                    res = parse_article(html)
                    name = urllib.parse.quote_plus(keyword)
                    with open(os.path.join(self.keyword_path,f"{name}.txt"), 'w') as f:
                        f.write(res)  
                    self.visited.append(name)
            except Exception as e:
                print(e)

