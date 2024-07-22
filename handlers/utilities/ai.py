# from openai import OpenAI


# class Assistant(OpenAI):

#     def client():

#         return OpenAI()

#     def message(persona=None,
#                 model=None,
#                 message=None):

#         client = Assistant.client()

#         completion = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": persona},
#             {"role": "user", "content": message}
#             ]
#         )

#         return completion.choices[0].message