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

    return h5_path
    

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
    txt += f'\n原文链接: {h5f["url"][()].decode()}'
    txt += f'\n发布于 {h5f["published_time"][()].decode()}'
    txt += f'\n\n作者: {h5f["author"][()].decode()}'
    txt += f'\n{h5f["author_bio_chinese"][()].decode()}'
    txt += f'\n\n副标题: {h5f["subtitle_chinese"][()].decode()}'
    txt += f'\n\n摘要 (ChatGPT 生成): {h5f["summary_chinese"][()].decode()}'
    txt += f'\n\n正文 (主要为ChatGPT 翻译): \n{h5f["body_chinese"][()].decode()}'

    return txt


def translate_h5_file(h5_path, **kwargs):

    ff = h5py.File(h5_path, 'a')

    body = ff['body'][()].decode()
    prompt_s = ts.get_summary_prompt(body)
    ff.create_dataset('summary', data=ts.run_gpt(prompt=prompt_s, **kwargs))

    for key in ["title", "subtitle", "author_bio", "body", "summary"]:
        prompt = ts.get_simple_translate_prompt(txt=ff[key][()].decode())
        ff.create_dataset(f'{key}_chinese', 
                          data=ts.run_gpt(prompt=prompt,
                                            **kwargs))
    
    ff.close()


def save_text_files(h5_path):
    
    # get the save folde and file name
    save_folder, file_name = os.path.split(h5_path)
    fn = os.path.splitext(file_name)[0]
   
    # save english text
    txt_eng_path = os.path.join(save_folder, f'{fn}_eng.txt')
    if os.path.isfile(txt_eng_path):
        os.remove(txt_eng_path)
    with open(txt_eng_path, 'w', encoding='utf-8') as f_eng:
        f_eng.write(get_text_for_printing_eng(h5_path=h5_path))
    
    # save chinese text
    txt_chs_path = os.path.join(save_folder, f'{fn}_chs.txt')
    if os.path.isfile(txt_chs_path):
        os.remove(txt_eng_path)
    with open(txt_chs_path, 'w', encoding='utf-8') as f_chs:
        f_chs.write(get_text_for_printing_chs(h5_path=h5_path))


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
    # print(get_text_for_printing_eng(h5_path=h5_path))
    # print(get_text_for_printing_chs(h5_path=h5_path))



