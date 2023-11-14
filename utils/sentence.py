import openai
import os
import g4f
import logging
from dotenv import load_dotenv

load_dotenv()

async def sent(sent):
    openai.api_key = os.getenv("gpt")
    response = await openai.Completion.acreate(
    model="gpt-3.5-turbo-instruct",
    prompt=f"""Ты  - нейросеть, которая помогает людям развивать навыки коммуникации.
    Пользователь отправляет тебе предложение: {sent}
    Напиши пять тем для разговора, о которых можно поговорить на свидании, которые связаны с этим предложением""",
    max_tokens=1000,
    temperature=1
    )
    return response['choices'][0]['text']

#sentence('Я люблю спорт')
