import requests
import openai
import os
import logging
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration



async def Blip_GPT(photo):
    # ===Blip===
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    img_url = photo
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    # ===GPT===
    openai.api_key = os.getenv("gpt")
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=f"""Ты  - нейросеть, которая помогает людям развивать навыки коммуникации.
    Пользователь отправляет тебе предложение, описывающее происходящее на фотографии: {description}.
    Напиши пять тем для разговора, о которых можно поговорить на свидании, которые связаны с этой фотографией""",
    max_tokens=1000,
    temperature=1
    )

    return response['choices'][0]['text']

    
#Blip_GPT('https://735606.selcdn.ru/thumbnails/photos/2022/05/22/eulwo5kmck3qkvjj_1024.jpg')
