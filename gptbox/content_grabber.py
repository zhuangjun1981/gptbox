import os, json
from urllib import request
from bs4 import BeautifulSoup


def parse_html(url):
    """
    parse an html into several soup objects
    """
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def detect_domain(url):
    """
    detect the domain name from an URL.
    These domain can be used by ContentGrabber to extract useful 
    information from the soup.

    Currently the recognizable domains are: 
        'space.com'
    """

    padded_url = url + ' ' * 40

    if 'space.com' in padded_url[:40]:
        domain = 'space.com'
    elif 'spacenews.com' in padded_url[:40]:
        domain = 'spacenews.com'
    else:
        print('Cannot find recognizable domain from URL.')
        domain = None

    return domain
    

def get_clean_text_spacedotcom(url):
    """
    Extract useful text from a space.com url.

    :param url: string, url of the webpage
    :return text_dict: dictionary
        keys:
            url : str, url of the webpage
            domain : str, domain of the webpage
            title : str, title of the article
            author : str, author of the article
            author_bio : str, a paragraph of author bio
            author_url : str, url to the author page
            image_urls : list of str, urls of all article images
                the first should be the title image
            published_time : publication time of the article
            body : list of str, body text of the article
                at the location of each article image the item should be
                    [image# <image_id>]figure caption
                at the location of each sub-headline the item should be
                    [headline# <headline_size>]headline text
    """

    def clean_text(txt):
        """
        text cleaning specific to space.com
        """
        text_to_remove = ["Follow us on Twitter @Spacedotcom and on Facebook.",
                      " (opens in new tab)",
                      "Join our Space Forums to keep talking space on the latest missions, night sky and more! And if you have a news tip, correction or comment, let us know at: community@space.com."]

        for tor in text_to_remove:
            txt = txt.replace(tor, "")

        txt = txt.replace("\xa0", " ")
        txt = txt.replace("&nbsp;", " ")
        txt = txt.replace("\'", "'")
        return txt.strip()
    
    domain = detect_domain(url=url)
    if domain != 'space.com':
        print(f'Cannot recognize domain: {domain}. Returning None.')
        return None
    
    soup = parse_html(url=url)

    text_dict = {}
    text_dict['domain'] = domain
    text_dict['body'] = []
    text_dict['image_urls'] = []
    img_id = 0
    
    # get meta dictionary from embedded json text
    json_text = [scr for scr in soup.find_all('script') if scr.get("type")=="application/ld+json"][0]
    json_dict = json.loads(json_text.get_text())
    text_dict['title'] = json_dict["headline"]
    text_dict['url'] = json_dict["url"]
    
    try:
        text_dict['author'] = json_dict["author"]["name"]
        text_dict['author_url'] = json_dict["author"]["url"]
        text_dict['author_bio'] = clean_text(json_dict["author"]["description"])
    except TypeError:
        text_dict['author'] = json_dict["author"][0]["name"]
        text_dict['author_url'] = json_dict["author"][0]["url"]
        text_dict['author_bio'] = clean_text(json_dict["author"][0]["description"])

    text_dict['image_urls'].append(json_dict["image"]["url"])
    text_dict['published_time'] = json_dict["datePublished"][0:19]

    # add title figure caption into body
    title_fig_cap = soup.find('figcaption')
    text_dict["body"].append(f'[image#{img_id:02d}]{clean_text(title_fig_cap.get_text())}')
    img_id += 1

    # get other body text, subheadline, and image text
    body = soup.find_all('div')
    body = [b for b in body if b.get('id')=='article-body'][0]
    for chi in body.children:

        if chi.name == 'p':
            chi_txt = clean_text(chi.get_text())
            if not chi_txt.startswith('Related:'):
                text_dict['body'].append(chi_txt)
        elif str(chi.name).startswith('h'):
            txt = clean_text(chi.get_text())
            hsize = str(chi.name)[1]
            text_dict['body'].append(f'[headline#{hsize}]{txt}')
        elif chi.name == 'a':
            fig = chi.find('figure')
            pic = fig.find('picture')
            text_dict['image_urls'].append(pic.find_all('source')[1].get('data-srcset').split(',')[-1].split(" ")[1])
            caption = clean_text(fig.find('figcaption').get_text())
            text_dict['body'].append(f'[image#{img_id:02d}]{caption}')
            img_id += 1
    
    return text_dict


# todo: update this method
def get_clean_text_spacenews(url):
    """
    Extract useful text from a spacenews.com url.

    :param url: string, url of the webpage
    :return text_dict: dictionary, each value is a string
        keys:
            url : url of the webpage
            domain : domain of the webpage
            title : title of the article
            author : author of the article
            author_bio : a paragraph of author bio
            subtitle : a short description of the article
            title_image_url : url of the title image
            published_time : publication time of the article
                format should always be "yyyy-mm-dd-hh-mm-ss"
            body : body text of the article
    """

    domain = detect_domain(url=url)
    if domain != 'spacenews.com':
        print(f'Cannot recognize domain: {domain}. Returning None.')
        return None
    
    text_dict = {}
    text_dict['domain'] = domain
    
    soup = parse_html(url=url)

    # useful info from meta
    metas = soup.find('head').find_all('meta')
    
    for meta in metas:
        if meta.get('property') == 'og:title':
            text_dict['title'] = meta.get('content').strip()

        if meta.get('name') == 'author':
            text_dict['author'] = meta.get('content').strip()
            
        if meta.get('property') == 'og:description':
            text_dict['subtitle'] = meta.get('content').strip()
            
        if meta.get('property') == 'og:url':
            text_dict['url'] = meta.get('content').strip()
        
        if meta.get('property') == 'og:image':
            text_dict['title_image_url'] = meta.get('content').strip()
            
        if meta.get('property') == 'article:published_time':

            pt = meta.get('content').strip()
            pt = pt.replace('T', '-')
            pt = pt.replace(':', '-')
            pt = pt[:19]

            text_dict['published_time'] = pt
    
    article = []
    author_bio = []
    divs = soup.find_all('div')
    for div in divs:
        if div.get('class') is not None:
            if div.get('class')[0] == "entry-content":
                ps = div.find_all('p')
                for p in ps:
                    article.append(p.get_text().strip())
                
            elif div.get('class')[0] == "author-bio-text":
                for p in div.find_all('p'):
                    for a in p.find_all('a'):
                        a.decompose()
                    author_bio.append(p.get_text().strip())

    article = '\n'.join([a for a in article if a])
    author_bio = '\n'.join([a for a in author_bio if a])
    author_bio = '\n'.join([a.strip() for a in author_bio.split('\n') if a.strip()])
    
    text_dict['body'] = article
    text_dict['author_bio'] = author_bio

    return text_dict


def download_image(url, folder, filename=None):
    """
    download the web image into a specified folder
    :params url: string, url link to the image
    :params folder: string, path the saving folder
    :params filename: string, file name to be saved, 
                      if None, original file name will be used.
    """
    
    fn_original = os.path.split(url)[1]

    if filename is None:
        filename = fn_original
    else:
        filename = f'{filename}{os.path.splitext(fn_original)[1]}'

    request.urlretrieve(url, os.path.join(folder, filename))


def get_text_from_html(url):
    """
    get raw html text and clean text dictionary from a webpage

    :params url: str, url of the webpage
    :return text_dict: dictionary
        url : str, url of the webpage
        raw_text: str, raw html text of the webpage
        domain : str, domain of the webpage
        title : str, title of the article
        author : str, author of the article
        author_bio : str, a paragraph of author bio
        author_url : str, url to the author page
        image_urls : list of str, urls of all article images
            the first should be the title image
        published_time : publication time of the article
        body : list of str, body text of the article
            at the location of each article image the item should be
                [image# <image_id>]figure caption
            at the location of each sub-headline the item should be
                [headline# <headline_size>]headline text
    """
    soup = parse_html(url=url)
    domain = detect_domain(url=url)
    text_dict = {}
    text_dict['raw_text'] = soup.get_text()

    if domain is not None:

        if domain == 'space.com':
            clean_text_dict = get_clean_text_spacedotcom(url=url)
        elif domain == 'spacenews.com':
            clean_text_dict = get_clean_text_spacenews(url=url)
        else:
            clean_text_dict = {}
            print(f'Cannot recognize domain {domain}. Set clean_text_dict to be empty.')

    else:
        clean_text_dict = {}
        print('domain is None. Set clean_text_dict to be empth.')
    
    text_dict.update(clean_text_dict)
    return text_dict


if __name__ == "__main__":
    url = "https://www.space.com/spacex-starship-launch-debris-terrifying"
    
    cg = ContentGrabber()
    cg.get_text_from_html(url=url)
    # print(cg.raw_text)
    [print(f'{k}: {v}') for k, v in cg.clean_text_dict.items()]

    # img_url = cg.clean_text_dict['title_image_url']
    # download_image(url=img_url, folder=r"D:\temp", filename=None)

