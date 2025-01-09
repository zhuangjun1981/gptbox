import os, openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def run_gpt(prompt, model="gpt-3.5-turbo", **kwargs):
    messages = [
        {
            "role": "system",
            "content": "you are a professional translator, expert in translating English news articles to Chinese",
        },
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(model=model, messages=messages, **kwargs)

    return response.choices[0].message["content"]


def get_simple_translate_prompt(txt):
    prompt = f"""
Translate the text delimited with ``` into Chinese. 
When translating, try to do the following:
1. keep the text in square brackets as the original without translation.
2. for proper nouns and names, try translate them into Chinese but keep the 
original English in Chinese parenthesis "（）" right after the corresponding Chinese words.
But do not do this for the title.
3. if the proper nons has abbreviation, add the abbreviation 
after the full english name separated by Chinese comma ",". Both the original English words and 
English abbreviation should be in Chinese parenthesis "（）"。
Do not include this in title.
4. Make a new line for each paragraph in the translation.

Here is one example:

English text:
Europe's Hera asteroid probe heads for Mars after engine burn
https://www.space.com/space-exploration/launches-spacecraft/europes-hera-asteroid-probe-heads-for-mars-after-engine-burn
Published at 2024-11-15T21:11:06
[image#00]An animation of ESA's Hera probe firing its thrusters to propel it towards Mars. (Image credit: ESA-Science Office)
The Hera asteroid probe has passed a critical milestone on its journey to study the site of the first asteroid deflection test.
The European Space Agency (ESA) spacecraft fired its three orbital control thrusters for 13 minutes on Nov. 6, following a longer, 100-minute burn on Oct. 23, the agency announced in a statement on Nov. 8.

Chinese translation:
欧洲的赫拉小行星探测器在发动机点火后前往火星
https://www.space.com/space-exploration/launches-spacecraft/europes-hera-asteroid-probe-heads-for-mars-after-engine-burn
发布于2024年11月15日21:11:06
[image#00]ESA的赫拉探测器点火推进，驶向火星的动画。（图片来源：ESA-Science Office）
赫拉小行星探测器（Hera asteroid probe）在前往研究首次小行星偏转试验地点的旅程中通过了一个关键里程碑。
欧洲航天局（European Space Agency，ESA）的航天器在11月6日点燃了三个轨道控制推进器13分钟，继10月23日更长的100分钟燃烧后，该机构在11月8日的声明中宣布。


Here is another example:
English text:
Boeing Starliner astronauts will return to Earth in March 2025 after new NASA, SpaceX delay
https://www.space.com/space-exploration/human-spaceflight/boeing-starliner-astronauts-will-return-to-earth-in-march-2025-after-new-nasa-spacex-delay
Published at 2024-12-18T11:00:00

Summary: 
The Crew-10 mission to the ISS, initially set for February 2025, is delayed to late March to allow SpaceX to prepare a new Crew Dragon spacecraft. This extends Crew-9's stay, including astronauts Wilmore and Williams, to nine months. The delay highlights SpaceX's fleet expansion and NASA's mission flexibility.

Main text:

[image#00]NASA astronauts Butch Wilmore and Suni Williams have been in space since June 5, 2024.
(Image credit: NASA)
The astronaut duo who flew the first-ever crewed mission of Boeing's Starliner capsule will have to wait a little longer to rejoin us on Earth.
The next crew rotation mission to the International Space Station (ISS), SpaceX's Crew-10, has been delayed to no earlier than late March 2025, NASA announced on Tuesday (Dec. 17).

Chinese translation:
波音Starliner宇航员将在新的NASA和SpaceX延迟后于2025年3月返回地球
https://www.space.com/space-exploration/human-spaceflight/boeing-starliner-astronauts-will-return-to-earth-in-march-2025-after-new-nasa-spacex-delay
发布于2024年12月18日11:00:00

摘要：
原定于2025年2月的Crew-10任务被推迟到3月底，以便SpaceX准备一艘新的Crew Dragon（龙飞船）航天器。这延长了Crew-9的停留时间，包括宇航员威尔莫尔（Wilmore）和威廉姆斯（Williams），至九个月。此次延迟突显了SpaceX舰队的扩展和NASA任务的灵活性。

正文：

[image#00]NASA宇航员布奇·威尔莫尔（Butch Wilmore）和苏尼·威廉姆斯（Suni Williams）自2024年6月5日以来一直在太空中。（图片来源：NASA）

首次乘坐波音星际客机（Starliner）胶囊的载人任务的宇航员二人组将不得不再等一段时间才能重返地球。

下一次前往国际空间站（International Space Station，ISS）的宇航员轮换任务，SpaceX的Crew-10，已被推迟到不早于2025年3月底，NASA在周二（12月17日）宣布。

```{txt}```
"""
    return prompt


def get_summary_prompt(txt):
    prompt = f"""
Summarize the text delimited with ``` into 50 words.

```{txt}```
"""
    return prompt


def break_text_into_blocks(text, max_len=1500):
    para_list = text.split("\n")
    blocks = []
    curr_block = ""

    for para in para_list:
        if len(curr_block) + len(para) < max_len:
            curr_block += f"{para}\n"
        else:
            blocks.append(curr_block)
            curr_block = f"{para}\n"

    blocks.append(curr_block)
    return blocks


def translate_long_text(text, max_len=1500, **kwargs):
    blocks = break_text_into_blocks(text=text, max_len=max_len)

    tsed = []
    for block in blocks:
        prompt = get_simple_translate_prompt(txt=block)
        ts_block = run_gpt(prompt=prompt, **kwargs)
        tsed.append(ts_block)
    tsed = "\n".join(tsed)
    return tsed


if __name__ == "__main__":
    print(os.getenv("OPENAI_API_KEY"))
