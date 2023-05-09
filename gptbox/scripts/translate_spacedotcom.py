import os
import sys
curr_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.extend([os.path.dirname(curr_folder)])
import content_grabber as cg
import database_tools as dt


save_folder = r"G:\temp"
# url = "https://www.space.com/spacex-starship-launch-debris-terrifying"
# url = "https://www.space.com/nasa-voyager-mission-engineers-documentary"
# url = "https://www.space.com/voyager-1-45-year-launch-anniversary"
# url = "https://spacenews.com/esa-troubleshooting-juice-radar-antenna/"
# url = "https://www.space.com/voyager-2"
# url = "https://www.space.com/why-take-juice-spacecraft-eight-years-reach-jupiter"
url = "https://spacenews.com/chinas-mystery-reusable-spaceplane-lands-after-276-days-in-orbit/"

text_dict = cg.get_text_from_html(url=url)
h5_path = dt.save_html_content(text_dict=text_dict, folder=save_folder)

dt.translate_h5_file(h5_path=h5_path, 
                     model="gpt-3.5-turbo",
                     temperature=0)

# h5_path = r"G:\temp\2022-08-17_space.com.h5"
dt.save_text_files(h5_path)
