from groq import Groq
import os
import hal9 as h9
import json
import openai

from tool_calculator import calculate
from tool_game import build_game
from tool_generic import generic_reply
from tool_hal9 import hal9_reply
from tool_website import build_website
from tool_streamlit import build_streamlit

MODEL = "llama3-70b-8192"

prompt = input("")
h9.event('prompt', prompt)

messages = h9.load("messages", [])
messages.append({"role": "user", "content": prompt})
h9.save("messages", messages, hidden=True)

all_tools = [
  calculate,
  build_game,
  generic_reply,
  hal9_reply,
  build_website,
  build_streamlit
]

tools = h9.describe(all_tools, model = "llama")

completion = Groq().chat.completions.create(
  model = MODEL,
  messages = messages,
  temperature = 0,
  seed = 1,
  tools=tools,
  tool_choice="auto")

h9.complete(completion, messages = messages, tools = all_tools, show = False, model = "llama")

h9.save("messages", messages, hidden=True)
