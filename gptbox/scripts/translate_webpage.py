import os
import sys
curr_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.extend([os.path.dirname(curr_folder)])
import content_grabber as cg
import database_tools as dt


save_folder = r"G:\temp"
# save_folder = r"D:\temp"

# url = "https://www.space.com/spacex-starship-launch-debris-terrifying"
# url = "https://www.space.com/nasa-voyager-mission-engineers-documentary"
# url = "https://www.space.com/voyager-1-45-year-launch-anniversary"
# url = "https://spacenews.com/esa-troublseshooting-juice-radar-antenna/"
# url = "https://www.space.com/voyager-2"
# url = "https://www.space.com/why-take-juice-spacecraft-eight-years-reach-jupiter"
# url = "https://spacenews.com/chinas-mystery-reusable-spaceplane-lands-after-276-days-in-orbit/"
# url = "https://www.space.com/moon-time-lunar-clock-debate-wristwatch"
# url = "https://www.space.com/nasa-selects-blue-origin-second-artemis-moon-lander"
# url = "https://www.space.com/18377-new-horizons.html"
# url = "https://www.space.com/nasa-juno-jupiter-io-volcanic-moon-images"
# url = "https://spacenews.com/exploration-upper-stage-unveiled-revolutionary-leap-in-crew-safety-cargo-capacity-and-deep-space-power"
# url = "https://www.space.com/gravitational-lensing-explained"
# url = "https://www.space.com/space-solar-power-satellite-beams-energy-1st-time"
# url = "https://www.space.com/euclid-spacecraft-named-after-mathematician"
# url = "https://www.space.com/starlink-satellite-conjunction-increase-threatens-space-sustainability"
# url = "https://www.space.com/how-long-could-you-survive-in-space-without-spacesuit"
# url = "https://www.space.com/largest-radio-telescope-smart-maintenance-robots"
# url = "https://www.space.com/soviet-satellite-breaks-apart-after-debris-strike"
# url = "https://www.space.com/what-are-kilonovas"
# url = "https://spacenews.com/nasa-starts-reassessment-of-mars-sample-return-architecture/"
# url = "https://www.space.com/china-worlds-largest-underwater-telescope-hunt-for-elusive-ghost-particles"
# url = "https://www.space.com/expert-voice-what-is-an-attosecond"
# url = "https://www.space.com/spacex-starship-second-test-flight-launch-explodes"
# url = "https://www.space.com/space-force-x-37b-spacex-falcon-heavy-1st-launch-dec-2023"
# url = "https://spacenews.com/nasa-slows-down-work-on-mars-sample-return-due-to-budget-uncertainty/"
# url = "https://spacenews.com/satellite-imagery-reveals-explosion-at-chinas-jiuquan-spaceport/"
# url = "https://spacenews.com/china-makes-progress-on-raptor-like-engines-for-super-heavy-rocket/"
# url = "https://www.space.com/what-are-radio-galaxies"
# url = "https://www.space.com/nasa-x-59-quesst-paint-job"
# url = "https://www.space.com/mars-rotor-system-test-nears-supersonic-speeds-ingenuity-flies-coincides"
url = "https://www.space.com/china-space-plane-depoyed-mystery-objects"



text_dict = cg.get_text_from_html(url=url)
h5_path = dt.save_html_content(text_dict=text_dict, folder=save_folder)

dt.translate_h5_file(h5_path=h5_path, 
                     model="gpt-4-1106-preview",
                    #  model="gpt-3.5-turbo",
                     max_len=10000,
                     temperature=0)

dt.save_text_files(h5_path)
