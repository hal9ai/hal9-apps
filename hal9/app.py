from groq import Groq
import os
import hal9 as h9
import json
import openai

from tool_calculator import calculate
from tool_game import build_game

MODEL = "llama3-70b-8192"

prompt = input("")
h9.event('prompt', prompt)

system_prompt = open('system.txt', 'r').read()

messages = h9.load("messages", [{"role": "system", "content": system_prompt}])
messages.append({"role": "user", "content": prompt})

tools = h9.describe([
  calculate,
  build_game
])

tools = [{ "type": "function", "function": tool} for tool in tools]

response = Groq().chat.completions.create(
  model = MODEL,
  messages = messages,
  temperature = 0,
  seed = 1,
  tools=tools,
  tool_choice="auto")

response_message = response.choices[0].message

tool_calls = response_message.tool_calls
if tool_calls:
    available_functions = {
        "calculate": calculate,
        "build_game": build_game
    }

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = str(function_to_call(**function_args))

        print(function_response)
        messages.append({"role": "assistant", "content": function_response})
else:
  response = Groq().chat.completions.create(model = MODEL, messages = messages, temperature = 0, seed = 1)
  response = response.choices[0].message.content

  print(response)
  messages.append({"role": "assistant", "content": response})

h9.save("messages", messages, hidden=True)
