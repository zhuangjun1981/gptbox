from urllib.request import urlopen
from bs4 import BeautifulSoup

def grab_text_from_url(url):

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
    
    txt = grab_text_from_url(url=url)
    txt_cleaner = TextCleaner()
    txt = TextCleaner.basic_cleaning(txt=txt)
    print(txt)