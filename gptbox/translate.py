import os, openai

curr_folder = os.path.dirname(os.path.realpath(__file__))

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key_path = os.path.join(curr_folder, "meta", "api_key.txt")


def translate(prompt, model="gpt-3.5-turbo", **kwargs):

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        **kwargs
    )

    return response.choices[0].message["content"]


def get_simple_translate_prompt(txt):

    prompt = f"""
    Translate the text between the three backticks into Chinese. \
But but do not translate names, locations, and other proper \
nouns, such as Startbase, Texas, Port Isabel, etc.  

    ```{txt}```
    """
    return prompt


def get_body_prompt(body):
    
    prompt = f"""
    1. Translate the text between the three backticks into Chinese in \
a semi-formal tone but do not translate names, locations, and other proper \
nouns, such as Startbase, Texas, Port Isabel, etc.
    2. Summarize the text between the three backticks into 50 words as summary.
    3. Translate the summary generated in step 2 into Chinese, but keep names, \
addresses, and other proper nouns as English. 

    retrun the results as json format with keys: body_chinese, summary, summary_chinese

    ```{body}```
    """

    return prompt


if __name__ ==  '__main__':

    import h5py

    file_path = r"G:\temp\2023-04-21_space.com.h5"
    ff = h5py.File(file_path, 'r')
    body = ff['body'][()].decode()
    title = ff['title'][()].decode()

    # print(title)
    # prompt_t = get_simple_translate_prompt(txt=title)
    # print(translate(prompt=prompt_t))

    # # print(body)
    # ps = body.split('\n')
    # paragraph = ps[3]
    # prompt_b = get_body_prompt(body=paragraph)
    # # print(prompt_b)
    # res = translate(prompt=prompt_b, 
    #                 temperature=0)

    # import json
    # aa = """
    # {
    #     "aa": 12,
    #     "bb": 13,
    #     "cc": "hello"
    # }
    # """
    # print(json.loads(aa)["aa"])