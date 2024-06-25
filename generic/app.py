import openai
import os

client = openai.AzureOpenAI(
  azure_endpoint = 'https://openai-hal9.openai.azure.com/',
  api_key = os.environ['OPENAI_AZURE'],
  api_version = '2023-05-15',
)

stream = client.chat.completions.create(
  model = "gpt-4",  # ID of the model to use.["gpt-4", "gpt-35-turbo", "gpt-35-turbo-16k"]
  # The messages parameter is an array of message objects, each having a role (system, user, or assistant) and content (the actual text of the message).
  # system: The system role typically provides high-level instructions or context-setting messages
  # user: The user role represents the messages or queries from the user or end-user interacting with the model.
  # assistant: The assistant role represents the responses generated by the ChatGPT model.
  messages = [
    {"role": "system", "content": """${prompt}"""},
    {"role": "user", "content": input("")},
  ],
  temperature = 0, # The temperature parameter influences the randomness of the generated responses. The default is 1, and it can be set between 0 and 2.
  top_p = 1, # The top_p parameter, An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
  frequency_penalty = 0, #helps reduce the chance of repeatedly sampling the same sequences of tokens. This parameter instructs the language model not to use the same words too frequently. Number between -2.0 and 2.0. , Defaults 0
  # We generally recommend altering frequency_penalty or temperature but not both.
  n = 1, # How many completions to generate for each prompt. Note: with stream = True, Hal9 UI only supports 1 response
  max_tokens= 4096 ,# The max_tokens parameter allows you to limit the length of the generated response. 1 token is approximately 4 characters or 0.75 words for English text.
  presence_penalty= 0 , # presence_penalty can be used to encourage the model to use a diverse range of tokens in the generated text. It instructs the language model to utilize different words, promoting variety in the outputs. Number between -2.0 and 2.0, default 0
  seed= 123456789, # Is still in a beta feature, but it allows you to obtain consistent results for every input submitted to GPT.
  stream = True, # The output is returned progressively, which gives the appearance that the response is being written in sections in the chat
  )


for chunk in stream:
  if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None: 
    print(chunk.choices[0].delta.content, end="")
