import os, h5py, json
import content_grabber as cg
import translate as ts

def save_html_content(article, folder):
    """
    :params article: content_grabber.ContentGrabber object
    """
    
    pub_time = article.clean_text_dict['published_time']
    domain = article.clean_text_dict['domain']
    title_img_url = article.clean_text_dict['title_image_url']
    fn = f'{pub_time[0:10]}_{domain}'

    h5_path = os.path.join(folder, f'{fn}.h5')
    # print(h5_path)

    # save title image
    cg.download_image(url=title_img_url, folder=folder, filename=fn)

    if os.path.isfile(h5_path):
        os.remove(h5_path)
    h5f = h5py.File(h5_path, 'a')
    for k, v in article.clean_text_dict.items():
        h5f.create_dataset(k, data=v)
    h5f.close()
    

def get_text_for_printing_eng(h5_path):

    h5f = h5py.File(h5_path, 'r')

    txt = ''
    txt += f'{h5f["title"][()].decode()}'
    txt += f'\n{h5f["url"][()].decode()}'
    txt += f'\nPublished at {h5f["published_time"][()].decode()}'
    txt += f'\n\nAuthor: {h5f["author"][()].decode()}'
    txt += f'\n{h5f["author_bio"][()].decode()}'
    txt += f'\n\nSubtitle: {h5f["subtitle"][()].decode()}'
    txt += f'\n\nSummary (ChatGPT generated): {h5f["summary"][()].decode()}'
    txt += f'\n\n{h5f["body"][()].decode()}'

    return txt


def get_text_for_printing_chs(h5_path):

    h5f = h5py.File(h5_path, 'r')

    txt = ''
    txt += f'{h5f["title_chinese"][()].decode()}'
    txt += f'\n{h5f["url"][()].decode()}'
    txt += f'\n发布于 {h5f["published_time"][()].decode()}'
    txt += f'\n\n作者: {h5f["author"][()].decode()}'
    txt += f'\n{h5f["author_bio_chinese"][()].decode()}'
    txt += f'\n\n副标题: {h5f["subtitle_chinese"][()].decode()}'
    txt += f'\n\n摘要 (ChatGTP 生成): {h5f["summary_chinese"][()].decode()}'
    txt += f'\n\n{h5f["body_chinese"][()].decode()}'

    return txt


def translate_h5_file(h5_path, **kwargs):

    ff = h5py.File(h5_path, 'a')

    for key in ["title", "subtitle", "author_bio"]:
        prompt = ts.get_simple_translate_prompt(txt=ff[key][()].decode())
        ff.create_dataset(f'{key}_chinese', 
                          data=ts.translate(prompt=prompt,
                                            **kwargs))
    
    prompt_body = ts.get_body_prompt(body=ff["body"][()].decode())
    resp_body = ts.translate(prompt=prompt_body, **kwargs)
    resp_body = json.loads(resp_body)
    for key, value in resp_body.items():
        ff.create_dataset(key, data=value)
    
    ff.close()


if __name__ == "__main__":
    
    # url = "https://www.space.com/spacex-starship-launch-debris-terrifying"
    # url = "https://www.space.com/spacex-starship-damage-starbase-launch-pad"
    # url = "https://www.space.com/nasa-voyager-mission-engineers-documentary"
    # save_folder = r"D:\temp"

    # article = cg.ContentGrabber()
    # article.get_text_from_html(url=url)
    # save_html_content(article=article, folder=save_folder)

    # h5_path = r"G:\temp\2023-04-21_space.com.h5"
    # translate_h5_file(h5_path)

    h5_path = r"G:\temp\2023-04-21_space.com.h5"
    print(get_text_for_printing_eng(h5_path=h5_path))
    # print(get_text_for_printing_chs(h5_path=h5_path))



