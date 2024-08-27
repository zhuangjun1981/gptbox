import os, openai

curr_folder = os.path.dirname(os.path.realpath(__file__))

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key_path = os.path.join(curr_folder, "meta", "api_key.txt")


def run_gpt(prompt, model="gpt-3.5-turbo", **kwargs):

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        **kwargs
    )

    return response.choices[0].message["content"]


def get_simple_translate_prompt(txt):

    prompt = f"""
Translate the text delimited with triple backticks into Chinese. \
Keep the text delimited in square brackets. \
Make a new line for each paragraph in the translation. \
Keep the summary within 120 chinese characters, including punctuations.

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

    para_list = text.split('\n')
    blocks = []
    curr_block = ''

    for para in para_list:

        if len(curr_block) + len(para) < max_len:
            curr_block += f'{para}\n'
        else:
            blocks.append(curr_block)
            curr_block = f'{para}\n'
    
    blocks.append(curr_block)
    return blocks


def translate_long_text(text, max_len=1500, **kwargs):

    blocks = break_text_into_blocks(text=text, max_len=max_len)

    tsed = []
    for block in blocks:
        prompt = get_simple_translate_prompt(txt=block)
        ts_block = run_gpt(prompt=prompt, **kwargs)
        tsed.append(ts_block)
    tsed = '\n'.join(tsed)
    return tsed

if __name__ ==  '__main__':

    # import h5py
    # file_path = r"G:\temp\2023-04-21_space.com.h5"
    # ff = h5py.File(file_path, 'r')
    # body = ff['body'][()].decode()
    # title = ff['title'][()].decode()

    # print(title)
    # prompt_t = get_simple_translate_prompt(txt=title)
    # print(run_gpt(prompt=prompt_t))

    fp = r"G:\temp\2022-08-17_space.com_eng.txt"
    with open(fp, 'r', encoding='UTF-8') as f:
        txt = f.readlines()
    txt = '\n'.join(txt)
    blocks = break_text_into_blocks(txt)
    [print(f'```{b}```') for b in blocks]


