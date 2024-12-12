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
Do not include this in title.
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
