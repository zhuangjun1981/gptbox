from urllib.request import urlopen
from bs4 import BeautifulSoup


def extract_text_from_url(url):

    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # # break into lines and remove leading and trailing space on each
    # lines = (line.strip() for line in text.splitlines())
    # # break multi-headlines into a line each
    # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # # drop blank lines
    # text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def extract_article_text_from_url(url):

    # Send a request to the website
    html = urlopen(url).read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, features="html.parser")
    
    # Find the main article content
    article = soup.find('article')
    
    # Find all unwanted elements such as ads, links, buttons etc.
    unwanted_tags = ['aside', 'script', 'style', 'footer']
    for tag in unwanted_tags:
        for element in article.find_all(tag):
            element.decompose()
    
    # Extract the text from the article and return it
    return article.get_text().strip()


class TextCleaner(object):

    def __init__(self):
        return
    
    @staticmethod
    def basic_cleaning(txt):

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in txt.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        txt = '\n'.join(chunk for chunk in chunks if chunk)

        return txt


if __name__ == "__main__":
    url = "https://www.space.com/spacex-starship-launch-debris-terrifying"
    
    # txt = grab_text_from_url(url=url)
    # txt_cleaner = TextCleaner()
    # txt = TextCleaner.basic_cleaning(txt=txt)

    txt = extract_article_text_from_url(url=url)
    print(txt)