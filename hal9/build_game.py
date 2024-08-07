import openai
import os
import hal9 as h9
import json

client = openai.AzureOpenAI(
    azure_endpoint='https://openai-hal9.openai.azure.com/',
    api_key=os.environ['OPENAI_AZURE'],
    api_version='2023-05-15',
)

def build_game(user_game_request):
   """
   Build a complex video game from a short text description.
     'user_game_request' is the requested user game to build.
   """
   number_of_steps = 5

   print('Generating custom prompt...')

   prompt_text = client.chat.completions.create(
      model="gpt-4",
      messages=[{"role": "user", "content": f"(Do not mention preloaded assets within the array) Make a string array of only text in JSON format that includes {number_of_steps} text elements where each text element describes an important instruction for generating the following user request as a pure single page HTML game: {user_game_request}, The JSON array must be flat and only contain strings"}],
      temperature=0,
   )

   response = prompt_text.choices[0].message.content
   prompts = h9.extract(markdown=response, language="json")
   prompts = json.loads(prompts)

   print(f"""This is the custom prompt I have generated for your game: {prompts}\n\n""")

   messages = h9.load("messages", [{"role": "system", "content": "Always reply with a single page HTML markdown block (which can use JavaScript, CSS, etc) that fulfills the user request and only use geometric shapes and colors for the single page HTML markdown block"}])

   print('For each step I complete there will be a generated game to go along with it! So you can see the progress of the game I am creating!')
   print('Generating game... \n\n')

   def improve_code(messages, prompt):
      messages.append({"role": "user", "content": prompt})
       
      completion = client.chat.completions.create(
         model="gpt-4",
         messages=messages,
         temperature=0,
      )
       
      response = completion.choices[0].message.content
      messages.append({"role": "assistant", "content": response})

      code = h9.extract(markdown=response, language="html")
      return code

   for i, prompt in enumerate(prompts):

      formatted_prompt = prompt.format(user_game_request=user_game_request)
      
      if (i == 0):
         code = improve_code(messages, formatted_prompt)
      else:
         code = improve_code(messages, f"""Fix/improve the following code by following the instruction:

   ```html
   {code}
   ```

   Instruction: {formatted_prompt} (Avoid Placeholders: Ensure the code is complete and functional, avoiding the use of placeholders.)
   """)

      print(f'Game iteration number {i + 1}:')
      h9.save(f"app{i}.html", code, hidden=False)

      print(f"Step {i+1} (Out of {number_of_steps}) completed successfully.")

   print('The final game is complete.')

   h9.save("messages", messages, hidden=True)
