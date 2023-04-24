import os
import openai

curr_folder = os.path.dirname(os.path.realpath(__file__))

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key_path = os.path.join(r"meta/api_key.txt")

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Translate this into 1. French, 2. Spanish and 3. Japanese:\n\nWhat rooms do you have available?\n\n1.",
  temperature=0.3,
  max_tokens=100,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)