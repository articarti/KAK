import whisper
import openai
import os
import logging
from dotenv import load_dotenv
load_dotenv()

async def audio(transcript, word):
    #audio_file= open(audio, "rb")
    #transcript = openai.Audio.translate(model="whisper-1", file="openai.mp3", response_format="text")

    openai.api_key = os.getenv("gpt")
    response = await openai.Completion.acreate(
    model="gpt-3.5-turbo-instruct",
    prompt=f"""Это мой рассказ о слове {word}: {transcript}. Напиши свою версию рассказа о {word}, но чтобы это было красочно, с эпитетами и харизматично""",
    max_tokens=1000,
    temperature=1
    )
    return response['choices'][0]['text']
