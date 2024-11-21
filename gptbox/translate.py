import os, openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def run_gpt(prompt, model="gpt-3.5-turbo", **kwargs):
    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(model=model, messages=messages, **kwargs)

    return response.choices[0].message["content"]


def get_simple_translate_prompt(txt):
    prompt = f"""
Translate the text delimited with triple backticks into Chinese. \
Keep the text delimited in square brackets. \
Make a new line for each paragraph in the translation. \

```{txt}```
"""
    return prompt


def get_summary_prompt(txt):
    prompt = f"""
Summarize the text delimited with triple backticks into 50 words.

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
