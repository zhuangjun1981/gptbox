import os
import h5py
import json
import requests
from wx_utils import get_wx_token


def remove_tag(line: str) -> str:
    """
    remove the bracket tag from the line text
    """
    idx0 = line.index("[")
    idx1 = line.index("]")
    return line[:idx0] + line[idx1 + 1 :]


def process_image_caption_line(line: str, img_meta_list: list[dict]) -> str:
    idx = line.index("]")
    img_idx = int(line[idx - 2 : idx])
    img_url = img_meta_list[img_idx]["url"]
    caption = line[idx + 1 :]
    line = f'</br></br><img src="{img_url}" align="center">'
    line += (
        '<p style="text-align: center"><span style="font-size: 14px" align="center">'
        + caption
        + "</span></p>"
    )
    return line


def merge_image_captions(lines: list[str]) -> list[str]:
    """
    the image caption in some translations have two lines
    if this is the case merge them into one line.
    """
    idx = 0
    while idx < len(lines):
        curr_line = lines[idx]
        if curr_line.startswith("[图片#"):  # caption line 1
            if lines[idx + 1].startswith("（"):  # caption line 2
                lines[idx] = lines[idx] + lines[idx + 1]
                lines.pop(idx + 1)
        idx += 1


def upload_image(img_path):
    """
    upload one image to weichat public account and return metadata

    Returns:
        meta_data: dictionary
          "media_id": str
          "url": str
    """
    # as permenant material
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={get_wx_token()}&type=image"

    # # as temporal material, valid for three days, for testing
    # url = f"https://api.weixin.qq.com/cgi-bin/material/upload?access_token={get_wx_token()}&type=image"

    # # as permenant image, does not return media_id, do not use
    # url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={get_wx_token()}"

    if img_path.endswith(".webp"):
        new_img_path = img_path[:-5] + ".jpg"
        os.rename(img_path, new_img_path)
        img_path = new_img_path

    _, img_fn = os.path.split(img_path)

    request_file = {
        "media": ((img_fn), open(img_path, "rb")),
    }

    print(f"uploading image: {img_path}")
    wx_res = requests.post(url=url, files=request_file)
    obj = json.loads(wx_res.content)
    return obj


def upload_images(folder):
    """
    upload all the images in the folder ordered by file name and return a list of medial metadata.
    image files are identified as having "_img" in the file name

    Returns:
      mata_list: list
    """
    img_fns = [fn for fn in os.listdir(folder) if "_img" in fn]
    img_fns.sort()

    meta_list = []
    for img_fn in img_fns:
        img_path = os.path.join(folder, img_fn)
        curr_meta = upload_image(img_path)
        meta_list.append(curr_meta)

    return meta_list


def delete_uploaded_media(media_id):
    data = {"media_id": media_id}
    url = f" https://api.weixin.qq.com/cgi-bin/material/del_material?access_token={get_wx_token()}"
    wx_res = requests.post(url=url, data=json.dumps(data))
    obj = json.loads(wx_res.content)
    if obj["errcode"] != 0:
        print(f"Cannot delete image ({media_id}). \n{obj}")


def delete_uploaded_medias(meta_list):
    for meta in meta_list:
        if "media_id" in meta:
            media_id = meta["media_id"]
            print(f"deleting {media_id} ...")
            delete_uploaded_media(media_id)
            # print("deleted.")


def parse_text(text, img_meta_list):
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    text_parts = {}

    lines = text.split("\n")
    lines = [l for l in lines if len(l) > 0]
    merge_image_captions(lines)

    text_parts["title"] = lines[0]
    text_parts["article_url"] = lines[1]
    text_parts["post_timestamp"] = lines[2]

    line_i = 0
    is_author_line = False
    while line_i < len(lines):
        if line_i == 0:  # title line
            lines[line_i] = "<p><span>" + lines[line_i] + "</span></p>"
        elif line_i == 1:  # url and post time line
            lines[1] = '<p><span style="font-size: 14px">' + lines[1] + "</span></p>"
            lines[1] += '<p><span style="font-size: 14px">' + lines[2] + "</span></p>"
            lines.pop(2)
        elif lines[line_i].startswith("摘要："):  # abstract line
            line = (
                '</br></br><p><span style="font-weight: bold; color: #007AAA">'
                + lines[line_i]
                + "</span></p>"
            )
            line += (
                '<p><span style="color: #007AAA">' + lines[line_i + 1] + "</span></p>"
            )
            lines[line_i] = line
            lines.pop(line_i + 1)
        elif lines[line_i].startswith("正文："):  # body line
            lines[line_i] = (
                '</br></br><p><span style="font-weight: bold">'
                + lines[line_i]
                + "</span></p>"
            )
        elif lines[line_i].startswith("[标题#"):  # section line
            lines[line_i] = (
                '</br></br><p style="text-align: center"><span style="font-size: 18px; font-weight: bold; color: #007AAA" align="center">'
                + remove_tag(lines[line_i])
                + "</span></p>"
            )
        elif lines[line_i].startswith("[图片#"):
            lines[line_i] = process_image_caption_line(
                lines[line_i], img_meta_list=img_meta_list
            )
        elif lines[line_i].startswith("作者："):
            lines[line_i] = (
                '</br></br><p><span style="font-size: 14px">'
                + lines[line_i]
                + "</span></p>"
            )
            is_author_line = True
        else:
            if is_author_line:
                lines[line_i] = (
                    '<p><span style="font_size: 14px">' + lines[line_i] + "</span></p>"
                )
            else:
                lines[line_i] = "</br><p><span>" + lines[line_i] + "</span></p>"

        line_i += 1

    # print("\n".join(lines))
    text_parts["body"] = "".join(lines[1:])

    return text_parts


def upload_draft(h5_path, should_clear_materials=False):
    assert os.path.isfile(h5_path), f"Cannot find h5 file from input path ({h5_path})."

    h5_f = h5py.File(h5_path, "r")
    text = h5_f["chinese_translate"][()].decode("utf-8")
    article_url = h5_f["url"][()].decode("utf-8")
    author = h5_f["author"][()].decode("utf-8")
    h5_f.close()

    if len(author) > 16:
        author_parts = author.split(" ")
        author = author_parts[0][0] + ". " + author_parts[-1]

    print("\nuploading images ...")
    folder, h5_fn = os.path.split(h5_path)
    img_meta_list = upload_images(folder)
    print("images uploaded.\n")

    print(f"\nposting {h5_path} to draft box ...")

    text_parts = parse_text(text, img_meta_list=img_meta_list)

    wxurl = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={get_wx_token()}"
    data = {
        "articles": [
            {
                "title": text_parts["title"],
                "author": author,
                "content": text_parts["body"],
                "thumb_media_id": img_meta_list[0]["media_id"],
                "content_source_url": article_url,
                "need_open_comment": 1,
            },
        ]
    }

    vx_res = requests.post(
        url=wxurl, data=json.dumps(data, ensure_ascii=False).encode("utf-8")
    )
    # obj = json.loads(vx_res.content)

    print("\ndraft posted.\n")

    if should_clear_materials:
        print("\ndeleting uploaded images ...")
        delete_uploaded_medias(img_meta_list)
        print("images deleted.")


if __name__ == "__main__":
    h5_path = (
        r"F:\webpage_translation\2024-11-11_space.com_00\2024-11-11_space.com_00.h5"
    )
    upload_draft(h5_path, should_clear_materials=True)
