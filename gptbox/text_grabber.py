from urllib.request import urlopen
from bs4 import BeautifulSoup


class TextGrabber(object):

    def __init__(self):
        self.clear()
    
    def clear(self):
        self.url = None
        self.domain = None
        self.raw_text = None
        self.clean_text_dict = None
    
    def detect_domain(self):

        padded_url = self.url + ' ' * 25

        if 'space.com' in padded_url[:25]:
            self.domain = 'space.com'
        else:
            print('Cannot find recognizable domain from URL.')
            self.domain = None
    
    def get_text_from_html(self, url):

        self.url = url
        self.detect_domain()

        if self.domain is not None:
            soup = self.parse_html()
            self.get_raw_text(soup=soup)
            self.get_clean_text(soup=soup)
        else:
            return
    
    def parse_html(self):
        html = urlopen(self.url).read()
        soup = BeautifulSoup(html, features="html.parser")
        return soup

    def get_raw_text(self, soup):
        self.raw_text = soup.get_text()

    def get_clean_text(self, soup):

        if self.domain is not None:
            if self.domain == 'space.com':
                self.clean_text_dict = self.get_clean_text_spacedotcom(soup=soup)
    
    @staticmethod
    def get_clean_text_spacedotcom(soup):

        # Find all unwanted elements such as ads, links, buttons etc.
        unwanted_tags = ['aside', 'script', 'style', 'footer']
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
                
        for element in soup.find_all('div'):
            if element.get('class') is not None:
                if element.get('class')[0] in ['more-about__cardBody']:
                    element.decompose()

        text_dict = {}

        # useful info from meta
        metas = soup.find('head').find_all('meta')

        for meta in metas:
            if meta.get('property') == 'og:title':
                text_dict['title'] = meta.get('content').strip()
                
            if meta.get('property') == 'og:description':
                text_dict['description'] = meta.get('content').strip()
                
            if meta.get('property') == 'og:url':
                text_dict['url'] = meta.get('content').strip()
                
            if meta.get('property') == 'article:published_time':
                text_dict['published_time'] = meta.get('content').strip()

        # useful stuff from p        
        ps = soup.find_all('p')
        # [print(p) for p in ps]

        article = []
        pi = 0
        while pi < len(ps):
            
            p = ps[pi]
            ptxt = p.get_text().strip()
            
            if p.get('class') is not None:
                if p.get('class')[0] in ['affiliate-disclaimer__copy', 'strapline',
                                        'newsletter-form__strapline', 'article__byline']:
                    pi += 1
                    continue
                
            if p.find('strong') is not None: # remove the section starts with "related"
                pi += 1
                continue
                
            if p.get('dir') == 'ltr': # remove twitter insert
                pi += 1
                continue
            
            if ptxt.startswith('—  '):
                pi += 1
                continue
                
            if ptxt.startswith('— '):
                pi += 1
                continue
                
            if p.find('em') is not None:
                pi += 1
                continue
                    
            article.append(ptxt)
            pi += 1
            
        article = '\n'.join([a for a in article if a])
        article = article.replace(" (opens in new tab)", "")

        text_dict['article'] = article

        # print('\n\n')
        # for key, value in stuff.items():
        #     print(f'{key}: {value}')

        return text_dict
            

if __name__ == "__main__":
    url = "https://www.space.com/spacex-starship-launch-debris-terrifying"
    
    tg = TextGrabber()
    tg.get_text_from_html(url=url)
    # print(tg.raw_text)
    [print(f'{k}: {v}') for k, v in tg.clean_text_dict.items()]
