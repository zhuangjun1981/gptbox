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


if __name__ ==  '__main__':

    import h5py

    file_path = r"G:\temp\2023-04-21_space.com.h5"
    # ff = h5py.File(file_path, 'r')
    # body = ff['body'][()].decode()
    # title = ff['title'][()].decode()

    # print(title)
    # prompt_t = get_simple_translate_prompt(txt=title)
    # print(run_gpt(prompt=prompt_t))


