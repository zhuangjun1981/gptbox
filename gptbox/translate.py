import os
import openai

curr_folder = os.path.dirname(os.path.realpath(__file__))

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key_path = os.path.join(curr_folder, "meta", "api_key.txt")

def translate_to_chinese(
        txt, model="text-davinci-003", temperature=0.3, 
        max_tokens=100, top_p=1.0, frequency_penalty=0.0,
        presence_penalty=0.0, **kwargs
        ):

    prompt = f'Translate this into Chinese:\n\n{txt}\n\n'

    response = openai.Completion.create(
        model=model, prompt=prompt, temperature=temperature, 
        max_tokens=max_tokens, top_p=top_p, 
        frequency_penalty=frequency_penalty, 
        presence_penalty=presence_penalty,
        **kwargs
        )
    
    return response


if __name__ ==  '__main__':
    
    txt = 'Hello world.'

    print(translate_to_chinese(txt=txt))
