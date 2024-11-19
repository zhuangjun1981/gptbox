import os, h5py, json
import content_grabber as cg
import translate as ts


def resolve_folder_path(folder_path):
    """
    resolve path if it already exists.
    1. add a suffix "_1" if it does not have a suffix
    2. update suffix by adding 1 if it has a suffix

    Return:
        folder_path: updated folder path
    """

    parent_folder, folder_n = os.path.split(folder_path)

    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    else:
        suffix = folder_n.split("_")[-1]

        try:
            suffix_int = int(suffix)
            folder_n = "_".join(folder_n.split("_")[:-1] + [str(suffix_int + 1)])
        except ValueError:
            folder_n = "_".join(folder_n.split("_")[:-1] + ["1"])

        folder_path = os.path.join(parent_folder, folder_n)
        os.makedirs(folder_path)

    return folder_path, folder_n


def save_html_content(text_dict, folder):
    """
    :params article: content_grabber.ContentGrabber object
    """

    pub_time = text_dict["published_time"]
    domain = text_dict["domain"]
    folder_n = f"{pub_time[0:10]}_{domain}"

    folder_path, fn = resolve_folder_path(os.path.join(folder, folder_n))
    h5_path = os.path.join(folder_path, f"{fn}.h5")
    # print(h5_path)

    # save images
    img_urls = text_dict["image_urls"]
    for img_i, img_url in enumerate(img_urls):
        cg.download_image(
            url=img_url, folder=folder_path, filename=f"{fn}_img{img_i:02d}"
        )

    if os.path.isfile(h5_path):
        os.remove(h5_path)
    h5f = h5py.File(h5_path, "a")
    for k, v in text_dict.items():
        h5f.create_dataset(k, data=v)
    h5f.close()

    return h5_path


def get_text_for_printing_eng(h5_path):
    h5f = h5py.File(h5_path, "r")

    txt = ""
    txt += f'{h5f["title"][()].decode()}'
    txt += f'\n{h5f["url"][()].decode()}'
    txt += f'\nPublished at {h5f["published_time"][()].decode()}'
    # txt += f'\n\nSummary (ChatGPT generated): \n{h5f["summary"][()].decode()}'
    # txt += '\n\nMain text (mainly translated by ChatGPT):\n'
    txt += f'\n\nSummary: \n{h5f["summary"][()].decode()}'
    txt += "\n\nMain text:\n"
    body = h5f["body"][()]
    for para in body:
        txt += f"\n{para.decode()}"
    txt += f'\n\nAuthor: {h5f["author"][()].decode()}'
    txt += f'\n{h5f["author_url"][()].decode()}'
    txt += f'\n{h5f["author_bio"][()].decode()}\n'

    return txt


def get_body_text_eng(h5_path):
    h5f = h5py.File(h5_path, "r")
    txt = ""
    for para in h5f["body"]:
        para_txt = para.decode()
        if not para_txt.startswith("["):
            txt += f"{para_txt}/n"
    h5f.close()
    return txt


def get_text_for_printing_chs(h5_path):
    h5f = h5py.File(h5_path, "r")
    txt = h5f["chinese_translate"][()].decode()
    h5f.close()
    return txt


def translate_h5_file(h5_path, max_len, **kwargs):
    ff = h5py.File(h5_path, "a")

    body_text = get_body_text_eng(h5_path=h5_path)
    prompt_s = ts.get_summary_prompt(body_text)
    ff.create_dataset("summary", data=ts.run_gpt(prompt=prompt_s, **kwargs))

    txt_eng = get_text_for_printing_eng(h5_path)
    # prompt = ts.get_simple_translate_prompt(txt=txt_eng)
    txt_chs = ts.translate_long_text(text=txt_eng, max_len=max_len, **kwargs)
    ff.create_dataset("chinese_translate", data=txt_chs)

    ff.close()


def save_text_files(h5_path):
    # get the save folde and file name
    save_folder, file_name = os.path.split(h5_path)
    fn = os.path.splitext(file_name)[0]

    # save english text
    txt_eng_path = os.path.join(save_folder, f"{fn}_eng.txt")
    if os.path.isfile(txt_eng_path):
        os.remove(txt_eng_path)
    with open(txt_eng_path, "w", encoding="utf-8") as f_eng:
        f_eng.write(get_text_for_printing_eng(h5_path=h5_path))

    # save chinese text
    txt_chs_path = os.path.join(save_folder, f"{fn}_chs.txt")
    if os.path.isfile(txt_chs_path):
        os.remove(txt_eng_path)
    with open(txt_chs_path, "w", encoding="utf-8") as f_chs:
        f_chs.write(get_text_for_printing_chs(h5_path=h5_path))


if __name__ == "__main__":
    # url = "https://www.space.com/spacex-starship-launch-debris-terrifying"
    # url = "https://www.space.com/spacex-starship-damage-starbase-launch-pad"
    # url = "https://www.space.com/nasa-voyager-mission-engineers-documentary"
    # save_folder = r"D:\temp"

    # article = cg.ContentGrabber()
    # article.get_text_from_html(url=url)
    # save_html_content(article=article, folder=save_folder)

    h5_path = r"G:\temp\2023-04-21_space.com.h5"
    translate_h5_file(h5_path)

    # h5_path = r"G:\temp\2023-04-21_space.com.h5"
    # print(get_text_for_printing_eng(h5_path=h5_path))
    # print(get_text_for_printing_chs(h5_path=h5_path))

    # h5_path = r"G:\temp\2023-05-08_spacenews.com.h5"
    # txt_eng = get_text_for_printing_eng(h5_path=h5_path)
    # blocks = ts.break_text_into_blocks(text=txt_eng, max_len=1500)
    # [print(f'\n\n\n{b}') for b in blocks]

    # path_org = r"F:\webpage_translation\2024-07-16_spacenews.com.h5"
    # print(resolve_path(path_org))

    # path_org = r"F:\webpage_translation\2024-07-16_spacenews.com_3.h5"
    # print(resolve_path(path_org))
