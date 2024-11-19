import os
import h5py
import json
import requests
from wx_utils import get_wx_token


def upload_image(img_path):
    token = get_wx_token()
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"

    _, img_fn = os.path.split(img_path)

    request_file = {
        "media": ((img_fn), open(img_path, "rb")),
    }
    try:
        wx_res = requests.post(url=url, files=request_file)
        obj = json.loads(wx_res.content)
        return obj["media_id"]
    except Exception as e:
        print(f"Error uploading image. {e}")
        return False


def upload_draft(h5_path):
    assert os.path.isfile(h5_path), f"Cannot find h5 file from input path ({h5_path})."

    folder, h5_fn = os.path.split(h5_path)
    fn, _ = os.path.splitext(h5_fn)

    img_fns = [
        f
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.startswith(fn) and "img" in f
    ]
    img_fns.sort()
    title_img_path = os.path.join(folder, img_fns[0])
    thumb_media_id = upload_image(title_img_path)

    # print(folder)
    # print(fn)
    # print(img_fns)

    token = get_wx_token()
    wxurl = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    data = {
        "articles": [
            {
                "title": "test_title",
                "author": "test_author",
                "content": "test_content",
                "thumb_media_id": thumb_media_id,
            },
        ]
    }
    vx_res = requests.post(
        url=wxurl, data=json.dumps(data, ensure_ascii=False).encode("utf-8")
    )

    obj = json.loads(vx_res.content)
    print(obj)


if __name__ == "__main__":
    upload_draft(
        r"F:\webpage_translation\2024-11-12_spacenews.com\2024-11-12_spacenews.com.h5"
    )
