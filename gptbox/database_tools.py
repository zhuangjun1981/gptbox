import os, h5py
import content_grabber as cg

def save_html_content(article, folder):
    """
    :params article: content_grabber.ContentGrabber object
    """
    
    pub_time = article.clean_text_dict['published_time']
    domain = article.clean_text_dict['domain']
    title_img_url = article.clean_text_dict['title_image_url']
    fn = f'{pub_time[0:10]}_{domain}'

    h5_path = os.path.join(folder, f'{fn}.h5')
    print(h5_path)

    # save title image
    cg.download_image(url=title_img_url, folder=folder, filename=fn)

    h5f = h5py.File(h5_path, 'a')
    for k, v in article.clean_text_dict.items():
        h5f.create_dataset(k, data=v)
    h5f.close()
    

if __name__ == "__main__":
    
    url = "https://www.space.com/spacex-starship-launch-debris-terrifying"
    save_folder = r"D:\temp"

    article = cg.ContentGrabber()
    article.get_text_from_html(url=url)
    save_html_content(article=article, folder=save_folder)

