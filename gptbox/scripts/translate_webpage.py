import os
import sys
curr_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.extend([os.path.dirname(curr_folder)])
import content_grabber as cg
import database_tools as dt

# save_folder = r"G:\temp"
# save_folder = r"D:\temp"
save_folder = r"F:\webpage_translation"

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
# url = "https://www.space.com/china-space-plane-depoyed-mystery-objects"
# url = "https://www.space.com/mars-rotor-system-test-nears-supersonic-speeds-ingenuity-flies-coincides"
# url = "https://www.space.com/15787-johannes-kepler.html"
# url = "https://www.space.com/nasa-removes-stuck-fasteners-osiris-rex-asteroid-samples"
# url = "https://www.space.com/astrobotic-peregrine-moon-lander-headed-to-earth"
# url = "https://spacenews.com/moores-law-space/"
# url = "https://spacenews.com/chinas-change-6-probe-arrives-at-spaceport-for-first-ever-lunar-far-side-sample-mission/"
# url = "https://www.space.com/solar-maximum-in-sight-but-scientists-will-have-to-wait-seven-months-after-it-occurs-to-officially-declare-it"
# url = "https://www.space.com/nasa-jpl-layoffs-february-2024-mars-sample-return"
# url = "https://www.space.com/nasa-voyager-spacecraft-mission-deep-space-update"
# url = "https://www.space.com/mars-ingenuity-helicopter-blade-mars-perseverance-photo"
# url = "https://www.space.com/spacex-starship-flight-3-launch-what-time"
# url = "https://www.space.com/spacex-starship-third-test-flight-launch"
# url = "https://spacenews.com/surprise-chinese-lunar-mission-hit-by-launch-anomaly/"
# url = "https://www.space.com/voyager-1-communications-update-fds-memory-issue"
# url = "https://spacenews.com/china-appears-to-be-trying-to-save-stricken-spacecraft-from-lunar-limbo/"
# url = "https://www.space.com/mars-giant-volcano-hiding-plain-sight"
# url = "https://www.space.com/object-crash-florida-home-iss-space-junk-nasa-confirms"
# url = "https://www.space.com/ingenuity-mars-helicopter-flight-map-video-2024"
# url = "https://www.space.com/china-reusable-rocket-aces-key-engine-tests"
# url = "https://www.space.com/china-tiangong-space-station-space-debris-measures"
# url = "https://www.space.com/what-is-solar-maximum-and-when-will-it-happen"
# url = "https://www.space.com/boeing-starliner-crew-flight-test-launch-pad-rollout"
# url = "https://www.space.com/boeing-starliner-nasa-astronauts-delay-emotional-rollercoaster-launch"
# url = "https://spacenews.com/chinas-change-6-is-carrying-a-surprise-rover-to-the-moon/"
# url = "https://www.space.com/satellite-images-rafah-israel-gaza"
# url = "https://www.space.com/spacex-crew-dragon-trunk-space-debris-canada"
# url = "https://www.space.com/voyager-1-mission-glitch-engineers-weighing-in-lucky-peanuts"
# url = "https://www.space.com/japan-slim-mission-unresponsive-jaxa-signal"
# url = "https://www.space.com/japanese-billionaire-cancels-spacex-starship-moon-dearmoon-flight"
# url = "https://www.space.com/boeing-starliner-crew-flight-test-launch"
# url = "https://www.space.com/spacex-starship-flight-4-test-launch-success"
# url = "https://spacenews.com/spacex-and-the-categorical-imperative-to-achieve-low-launch-cost/"
# url = "https://www.space.com/mars-water-frost-equator-exomars-tharsis-olympus-mons"
# url = "https://www.space.com/boeing-starliner-helium-leaks-assessment"
# url = "https://spacenews.com/voyager-1-returning-science-data-again/"
# url = "https://www.space.com/shenzhou-18-second-spacewalk-tiangong-space-debris-shield"
# url = "https://spacenews.com/europe-set-for-crucial-first-launch-of-ariane-6/"
# url = "https://www.space.com/what-are-blazars-complete-guide"
# url = "https://www.space.com/europe-clipper-transistors-vulnerable-radiation"
# url = "https://spacenews.com/china-reschedules-planetary-defense-mission-for-2027-launch/"
# url = "https://www.space.com/spacex-rocket-failure-nasa-astronaut-launch-schedule-iss"
# url = "https://www.space.com/iss-deorbit-destroy-spacex-vehicle-18-months"
url = "https://spacenews.com/china-prepares-to-launch-new-long-march-12-rocket/"

text_dict = cg.get_text_from_html(url=url)
h5_path = dt.save_html_content(text_dict=text_dict, folder=save_folder)

dt.translate_h5_file(h5_path=h5_path, 
                     model="gpt-4-1106-preview",
                    #  model="gpt-3.5-turbo",
                     max_len=100000,
                     temperature=0)

dt.save_text_files(h5_path)
