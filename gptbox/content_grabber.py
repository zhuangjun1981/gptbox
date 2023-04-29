import os
from urllib import request
from bs4 import BeautifulSoup


def parse_html(url):
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def detect_domain(url):

    padded_url = url + ' ' * 25

    if 'space.com' in padded_url[:25]:
        domain = 'space.com'
    else:
        print('Cannot find recognizable domain from URL.')
        domain = None

    return domain
    

def get_clean_text_spacedotcom(url):

    domain = detect_domain(url=url)
    if domain != 'space.com':
        print(f'Cannot recognize domain: {domain}. Returning None.')
        return None
    
    soup = parse_html(url=url)

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

        if meta.get('name') == 'parsely-author':
            text_dict['author'] = meta.get('content').strip()
            
        if meta.get('property') == 'og:description':
            text_dict['description'] = meta.get('content').strip()
            
        if meta.get('property') == 'og:url':
            text_dict['url'] = meta.get('content').strip()
        
        if meta.get('property') == 'og:image':
            text_dict['title_image_url'] = meta.get('content').strip()
            
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
    

def download_image(url, folder, filename=None):
    
    fn_original = os.path.split(url)[1]

    if filename is None:
        filename = fn_original
    else:
        filename = f'{filename}.{os.path.splitext(fn_original)[1]}'

    request.urlretrieve(url, os.path.join(folder, filename))


class ContentGrabber(object):

    def __init__(self):
        self.clear()
    
    def clear(self):
        self.url = None
        self.domain = None
        self.raw_text = None
        self.clean_text_dict = None
    
    def get_text_from_html(self, url):
        self.url = url
        soup = parse_html(url=url)
        self.domain = detect_domain(url=url)
        self.raw_text = soup.get_text()

        if self.domain is not None:

            if self.domain == 'space.com':
                self.clean_text_dict = get_clean_text_spacedotcom(url=url)
            else:
                self.clean_text_dict = None
                print(f'Cannot recognize domain {self.domain}. Set self.clean_text_dict to be None.')
        else:
            self.clean_text_dict = None
            print('self.domain is None. Set self.clean_text_dict to be None.')
            return
    

if __name__ == "__main__":
    url = "https://www.space.com/spacex-starship-launch-debris-terrifying"
    
    cg = ContentGrabber()
    cg.get_text_from_html(url=url)
    # print(cg.raw_text)
    [print(f'{k}: {v}') for k, v in cg.clean_text_dict.items()]

    img_url = cg.clean_text_dict['title_image_url']
    download_image(url=img_url, folder=r"C:\Users\wood_\Desktop", filename=None)

