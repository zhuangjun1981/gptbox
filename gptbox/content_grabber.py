import os
import json
import requests
from PIL import Image
from io import BytesIO
from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import quote


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

    padded_url = url + " " * 40

    if "space.com" in padded_url[:40]:
        domain = "space.com"
    elif "spacenews.com" in padded_url[:40]:
        domain = "spacenews.com"
    else:
        print("Cannot find recognizable domain from URL.")
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
        text_to_remove = [
            "Follow us on Twitter @Spacedotcom and on Facebook.",
            " (opens in new tab)",
            "Join our Space Forums to keep talking space on the latest missions, night sky and more! And if you have a news tip, correction or comment, let us know at: community@space.com.",
        ]

        for tor in text_to_remove:
            txt = txt.replace(tor, "")

        txt = txt.replace("\xa0", " ")
        txt = txt.replace("&nbsp;", " ")
        txt = txt.replace("'", "'")
        return txt.strip()

    domain = detect_domain(url=url)
    if domain != "space.com":
        print(f"Cannot recognize domain: {domain}. Returning None.")
        return None

    soup = parse_html(url=url)

    text_dict = {}
    text_dict["domain"] = domain
    text_dict["body"] = []
    text_dict["image_urls"] = []
    img_id = 0

    # get meta dictionary from embedded json text
    json_text = [
        scr
        for scr in soup.find_all("script")
        if scr.get("type") == "application/ld+json"
    ][0]
    json_dict = json.loads(json_text.get_text())
    text_dict["title"] = json_dict["headline"]
    text_dict["url"] = json_dict["url"]

    author_dict = json_dict["author"]
    if isinstance(author_dict, list):
        author_dict = author_dict[0]

    text_dict["author"] = author_dict["name"]

    if "url" in author_dict:
        text_dict["author_url"] = author_dict["url"]
    else:
        text_dict["author_url"] = ""

    if "description" in author_dict:
        text_dict["author_bio"] = clean_text(author_dict["description"])
    else:
        text_dict["author_bio"] = ""

    text_dict["image_urls"].append(json_dict["image"]["url"])
    text_dict["published_time"] = json_dict["datePublished"][0:19]

    # add title figure caption into body
    title_fig_cap = soup.find("figcaption")

    if title_fig_cap is not None:
        text_dict["body"].append(
            f"[image#{img_id:02d}]{clean_text(title_fig_cap.get_text())}"
        )
        img_id += 1

    # get other body text, subheadline, and image text
    body = soup.find_all("div")
    body = [b for b in body if b.get("id") == "article-body"][0]
    for chi in body.children:
        if chi.name == "p":
            chi_txt = clean_text(chi.get_text())
            if (not chi_txt.startswith("Related:")) and (
                not chi_txt.startswith("Read more")
            ):
                text_dict["body"].append(chi_txt)
        elif str(chi.name).startswith("h"):
            txt = clean_text(chi.get_text())
            hsize = str(chi.name)[1]
            text_dict["body"].append(f"[headline#{hsize}]{txt}")
        elif (chi.find("picture") is not None) and (chi.find("picture") != -1):
            if chi.name == "figure":
                fig = chi
            else:
                fig = chi.find("figure")
            pic = fig.find("picture")

            try:
                text_dict["image_urls"].append(
                    pic.find_all("source")[1]
                    .get("data-srcset")
                    .split(",")[-1]
                    .split(" ")[1]
                )
            except Exception as e:
                text_dict["image_urls"].append(
                    pic.find_all("source")[0].get("srcset").split(",")[-1].split(" ")[1]
                )

            caption = clean_text(fig.find("figcaption").get_text())
            text_dict["body"].append(f"[image#{img_id:02d}]{caption}")
            img_id += 1

    return text_dict


def get_clean_text_spacenews(url):
    """
    Extract useful text from a spacenews.com url.

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
                    [image#<image_id>]figure caption
                at the location of each sub-headline the item should be
                    [headline#<headline_size>]headline text
                at the location of each quote the item should be
                    [quote#<quote_id>]quote
    """

    domain = detect_domain(url=url)
    if domain != "spacenews.com":
        print(f"Cannot recognize domain: {domain}. Returning None.")
        return None

    def clean_text(txt):
        """
        text cleaning specific to space.com
        """
        text_to_remove = []
        for tor in text_to_remove:
            txt = txt.replace(tor, "")

        txt = txt.replace("\xa0", " ")
        txt = txt.replace("&nbsp;", " ")
        return txt.strip()

    img_id = 0
    quote_id = 0
    text_dict = {}
    text_dict["domain"] = domain
    text_dict["image_urls"] = []
    text_dict["body"] = []

    soup = parse_html(url=url)

    json_text = [
        j for j in soup.find_all("script") if j.get("type") == "application/ld+json"
    ][0]
    meta_dict = json.loads(json_text.get_text())["@graph"]

    # add meta
    text_dict["title"] = [d for d in meta_dict if d["@type"] == "Article"][0][
        "headline"
    ]
    text_dict["url"] = [d for d in meta_dict if d["@type"] == "Article"][0][
        "mainEntityOfPage"
    ]["@id"]
    text_dict["published_time"] = [d for d in meta_dict if d["@type"] == "Article"][0][
        "datePublished"
    ][0:19]
    text_dict["author"] = [d for d in meta_dict if d["@type"] == "Person"][0]["name"]
    text_dict["author_url"] = [d for d in meta_dict if d["@type"] == "Person"][0]["url"]
    try:
        text_dict["author_bio"] = clean_text(
            [d for d in meta_dict if d["@type"] == "Person"][0]["description"]
        )
    except KeyError:
        text_dict["author_bio"] = ""

    # add head figure
    headfigure = [
        f for f in soup.find_all("figure") if f.get("class")[0] == "post-thumbnail"
    ][0]
    text_dict["body"].append(
        f'[image#{img_id:02d}]{headfigure.find("figcaption").get_text()}'
    )
    text_dict["image_urls"].append(
        headfigure.find_all("img")[0].get("src").split("?")[0]
    )
    img_id += 1

    # add main article
    article = soup.find_all("div")

    article = [
        a
        for a in article
        if (a.get("class") is not None)
        and a.get("class")
        and (a.get("class")[0] == "entry-content")
    ][0]

    for chi in article.children:
        if chi.name == "p":
            chi_txt = clean_text(chi.get_text())
            if not chi_txt.startswith("Related:"):
                text_dict["body"].append(chi_txt)
        elif str(chi.name).startswith("h"):
            txt = clean_text(chi.get_text())
            hsize = str(chi.name)[1]
            text_dict["body"].append(f"[headline#{hsize}]{txt}")
        elif chi.name == "figure":
            if chi.find("blockquote") is not None:
                if type(chi.find("blockquote")) == list:
                    quote = chi.find("blockquote")[0]
                else:
                    quote = chi.find("blockquote")
                text_dict["body"].append(
                    f"[quote#{quote_id:02d}]{clean_text(quote.get_text())}"
                )
                quote_id += 1
            elif chi.find("img") is not None:
                text_dict["body"].append(
                    f'[image#{img_id:02d}]{clean_text(chi.find("figcaption").get_text())}'
                )
                text_dict["image_urls"].append(chi.find("img").get("src").split("?")[0])

                img_id += 1

    return text_dict


def download_image(url, folder, filename=None):
    """
    download the web image into a specified folder
    :params url: string, url link to the image
    :params folder: string, path the saving folder
    :params filename: string, file name to be saved,
                      if None, original file name will be used.
    """

    url = quote(url, safe=":/")

    fn_original = os.path.split(url)[1]

    if filename is None:
        filename = fn_original

    file_ext = "." + url.split(".")[-1]

    if file_ext != ".webp":
        request.urlretrieve(url, os.path.join(folder, filename + file_ext))
    else:
        response = requests.get(url)
        response.raise_for_status()
        with Image.open(BytesIO(response.content)) as img:
            rgb_img = img.convert("RGB")
            rgb_img.save(os.path.join(folder, filename + ".jpg"), "JPEG")


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
    text_dict["raw_text"] = soup.get_text()

    if domain is not None:
        if domain == "space.com":
            clean_text_dict = get_clean_text_spacedotcom(url=url)
        elif domain == "spacenews.com":
            clean_text_dict = get_clean_text_spacenews(url=url)
        else:
            clean_text_dict = {}
            print(f"Cannot recognize domain {domain}. Set clean_text_dict to be empty.")

    else:
        clean_text_dict = {}
        print("domain is None. Set clean_text_dict to be empth.")

    text_dict.update(clean_text_dict)
    return text_dict


if __name__ == "__main__":
    # url0 = "https://www.space.com/spacex-starship-launch-debris-terrifying"
    # url1 = "https://spacenews.com/chinas-mystery-reusable-spaceplane-lands-after-276-days-in-orbit/"
    # url2 = "https://spacenews.com/maxar-pursuing-defense-deals-for-its-new-line-of-small-satellites/"

    # print(get_text_from_html(url=url2))

    img_url0 = (
        "https://cdn.mos.cms.futurecdn.net/TyACrKUN6v7RgNfcKysgSQ-1200-80.jpg.webp"
    )
    img_url1 = (
        "https://cdn.mos.cms.futurecdn.net/YU8kxPCVpqGvkkNMDjv8m5-1200-80.jpg.webp"
    )
    folder = r"F:\webpage_translation\2024-11-11_space.com_00"
    fn0 = "2024-11-11_space.com_00_img01"
    fn1 = "2024-11-11_space.com_00_img02"

    download_image(img_url0, folder, fn0)
    download_image(img_url1, folder, fn1)
