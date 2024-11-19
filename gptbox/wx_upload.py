import os
import h5py
import json
import requests
from wx_utils import get_wx_token


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
    # if "errcode" in obj:
    #     print(f"Error uploading image. {obj}")
    print(obj)
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
            print("deleted.")


def parse_text(text):
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    text_parts = {}

    lines = text.split("\n")

    text_parts["title"] = lines[0]
    text_parts["article_url"] = lines[1]
    text_parts["post_timestamp"] = lines[2]

    author_line = [l for l in lines if l.startswith("作者：")][-1]
    text_parts["author"] = author_line.split("：")[-1]

    lines = ["<p>" + l + "</p><br/>" for l in lines]
    text_parts["body"] = "".join(lines[1:])

    return text_parts


def upload_draft(h5_path, should_clear_materials=False):
    assert os.path.isfile(h5_path), f"Cannot find h5 file from input path ({h5_path})."

    h5_f = h5py.File(h5_path, "r")
    text = h5_f["chinese_translate"][()].decode("utf-8")
    h5_f.close()

    folder, h5_fn = os.path.split(h5_path)
    img_meta_list = upload_images(folder)

    text_parts = parse_text(text)

    wxurl = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={get_wx_token()}"
    data = {
        "articles": [
            {
                "title": text_parts["title"],
                "author": text_parts["author"],
                "content": text_parts["body"],
                "thumb_media_id": img_meta_list[0]["media_id"],
            },
        ]
    }
    vx_res = requests.post(
        url=wxurl, data=json.dumps(data, ensure_ascii=False).encode("utf-8")
    )

    # obj = json.loads(vx_res.content)

    if should_clear_materials:
        delete_uploaded_medias(img_meta_list)


if __name__ == "__main__":
    h5_path = (
        r"F:\webpage_translation\2024-11-11_space.com_00\2024-11-11_space.com_00.h5"
    )
    upload_draft(h5_path, should_clear_materials=True)
