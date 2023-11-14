import os
import g4f
import torch
import openai
import logging
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("gpt")

async def chain_train(word):
    messages = [
        {"role": "system", "content": "Ты - нейросеть, которая помогает развивать навыки коммуникации."},
        {"role": "user", "content": f'давай сыграем в игру: я называю слово, а ты пишешь ближайшую, на твой взгляд, ассоциацию с этим словом (это должно быть существительное). Затем я пишу свое слово, и так по очереди. Начнем со слова {word}. Пиши только одно слово'}
    ]

    message = ''
    chain =[word]

    while message.lower() != "как дела":
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        message = input()
        messages.append({"role": "user", "content": message})

        chain.append(reply)
        chain.append(message)

        if message == 'как дела':
            messages.append({"role": "user", "content": f'у нас получилась такая цепочка слов: {"" "".join(chain)}. Напиши другие варианты цепочек, которыем могли бы получиться от слова {word}'})
            response = openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages)
            reply = response#["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": reply})

            return chain
#chain_train('кровать')

async def chain_learn(word):
    response = await openai.Completion.acreate(
    model="gpt-3.5-turbo-instruct",
    prompt=f"Напиши ассоциации к слову {word}. Каждую на новой строчке, начиная со знака - ",
    max_tokens=1000,
    temperature=1
    )

    return response['choices'][0]['text']

#chain_learn('Абрамович')
