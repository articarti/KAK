from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message, CallbackQuery, PhotoSize, voice
from lexicon.lexicon_ru import LEX, LEXICON_COMMANDS
from keyboards import kb
from states.states import Gen
from aiogram.methods.get_file import GetFile
from dotenv import load_dotenv
load_dotenv()
import os
from utils.blip import Blip_GPT
from utils.sentence import sent
from utils.audio import audio
from utils.chain import chain_train, chain_learn
from bot import bot
from files.csv_df import sentences, nouns, adjectives
from pydub import AudioSegment
from moviepy.editor import AudioFileClip
import openai


router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEX['/start'])

#Этот хэндлер срабатывает на команду /games
@router.message(Command(commands='games'))
async def process_games_command(message: Message):
    await message.answer(text='Описание игр')


#Photo--------------------------------------------------------------------------------------------
@router.message(Command(commands='image'), StateFilter(default_state))
async def process_yes_answer(message: Message):
    await message.answer(text=LEX['photo'], reply_markup=kb.photo_menu)


#Learn
@router.callback_query(F.data == 'photo_study', StateFilter(default_state))
async def photo_learn(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Вы выбрали режим 'Учеба' в игре 'Фото'. Отправьте фото")
    await state.set_state(Gen.img_learn)

@router.message(bot, StateFilter(Gen.img_learn), F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message, state: FSMContext, largest_photo: PhotoSize):
    file_info = await bot.get_file(largest_photo.file_id)
    photo_url = f"https://api.telegram.org/file/bot{os.getenv('tg')}/{file_info.file_path}"
    res = await Blip_GPT(photo_url)
    await message.answer(res)



#Train
@router.callback_query(F.data == 'photo_train', StateFilter(default_state))
async def on_photo_practice(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_train)
    # Здесь вы можете выполнить необходимые действия для режима "Практика" в игре "Фото"
    await callback.message.answer(text="Вы выбрали режим 'Практика' в игре 'Фото'.")
#-------------------------------------------------------------------------------------------------



#Audio--------------------------------------------------------------------------------------------
@router.message(Command(commands='audio'), StateFilter(default_state))
async def choice_audio(message: Message):
    await message.answer(text=LEX['audio'], reply_markup=kb.audio_menu)

    
@router.callback_query(F.data == 'audio_play', StateFilter(default_state))
async def audio_play(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Вы выбрали режим 'Игра' в игре 'Аудио'. Отправьте voice message")
    global audio_word
    audio_word = nouns.sample().values[0][0]
    await callback.message.answer(text=f"Слово:\n{audio_word}")
    await state.set_state(Gen.audio_play)


@router.message(StateFilter(Gen.audio_play), F.voice)
async def audio_play(message: Message, state: FSMContext):
    global audio_word
    voice_file = await bot.get_file(message.voice.file_id)
    downloaded_ogg = await bot.download_file(voice_file.file_path)

    # Сохраняем скачанный файл с расширением .ogg
    with open("voice_message.ogg", 'wb') as file:
        file.write(downloaded_ogg.read())

    audio_clip = AudioFileClip("voice_message.ogg")
    audio_clip.write_audiofile("voice_message.mp3")

    with open("voice_message.mp3", "rb") as audio_file:
        # Транскрибируем аудио с помощью OpenAI Whisper
        transcript = openai.Audio.transcribe("whisper-1", audio_file).text

        await message.answer(text=f'<b>Ваш рассказ:</b> \n{transcript}')
    #transcript = openai.Audio.transcribe("whisper-1", audio_file).text
    #ogg_audio = AudioSegment.from_ogg(downloaded_file)
    #mp3_audio = ogg_audio.export("voice_message.mp3", format="mp3")
    res = await audio(transcript, audio_word)
    await message.answer(res)
    audio_word = nouns.sample().values[0][0]
    await message.answer(text=f"Слово:\n{audio_word}")
#-------------------------------------------------------------------------------------------------





#Sentence----------------------------------------------------------------------------------------
@router.message(Command(commands='sentence'), StateFilter(default_state))
async def choice_sentence(message: Message):
    await message.answer(text=LEX['sentence'], reply_markup=kb.sentence_menu)

#Learn
@router.callback_query(F.data == 'sent_study', StateFilter(default_state))
async def sentence_learn(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Вы выбрали режим 'Учеба' в игре 'Предожение'.")
    await state.set_state(Gen.sent_learn)


@router.message(StateFilter(Gen.sent_learn), (F.text & F.text != '/stop'))
async def sentence_learn(message: Message, state: FSMContext):
    input = message.text 
    res = await sent(input)
    await message.answer(res)


#Train
@router.callback_query(F.data == 'sent_train', StateFilter(default_state))
async def sentence_train(callback: CallbackQuery, state: FSMContext):
    global sample
    sample = sentences.sample().values[0][0]
    await callback.message.answer(text=f"Вы выбрали режим 'Практика' в игре 'Предожение'")
    await callback.message.answer(text=f"Предлжение:\n{sample}")
    await state.set_state(Gen.sent_train)


@router.message(StateFilter(Gen.sent_train), (F.text & F.text != '/stop'))
async def sentence_train(message: Message, state: FSMContext):
    global sample
    input = sample
    res = await sent(sample)
    await message.answer(res)
    sample = sentences.sample().values[0][0]
    await message.answer(sample)

#-------------------------------------------------------------------------------------------------






#Chain---------------------------------------------------------------------------------------------
@router.message(Command(commands='chain'), StateFilter(default_state))
async def choice_chain(message: Message):
    await message.answer(text=LEX['chain'], reply_markup=kb.chain_menu)


#Play    
@router.callback_query(F.data == 'chain_play', StateFilter(default_state))
async def chain_play(callback: CallbackQuery, state: FSMContext):
    global chain_word, chain, messages
    chain_word = nouns.sample().values[0][0]
    chain = []
    messages = [
        {"role": "system", "content": "Ты - нейросеть, которая помогает развивать навыки коммуникации."},
        {"role": "user", "content": f'давай сыграем в игру: я называю слово, а ты пишешь ближайшую, на твой взгляд, ассоциацию с этим словом (это должно быть существительное). Затем я пишу свое слово, и так по очереди. Начнем со слова {chain_word}. Пиши только одно слово'}
    ]
    response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages)
    reply = response["choices"][0]["message"]["content"]
    await callback.message.answer(text=f"Вы выбрали режим 'Игра' в игре 'Цепочка ассоциаций'")
    await callback.message.answer(text=f"Первое слово:\n{reply}")
    chain.append(reply)
    await state.set_state(Gen.chain_play)


@router.message(StateFilter(Gen.chain_play), F.text)
async def chain_play(message: Message, state: FSMContext):
    word = message.text
    if word == '/stop':
        if len(chain) > 4:
            response = await openai.Completion.acreate(
                model="gpt-3.5-turbo-instruct",
                prompt=f"""Есть цепочка ассоциаций: {chain}. Напиши другие варианты цепочек, которыем могли бы получиться от слова {chain[0]}""",
                max_tokens=1000,
                temperature=1
                )
            reply = response['choices'][0]['text']
            await message.answer(reply)
            await message.answer(
                text='Вы вышли из игры'
            )
            await state.clear()
            return None
        await message.answer(
                    text='Вы вышли из игры')
        await state.clear()
        return None
    chain.append(word)
    messages.append({"role": "user", "content": word})
    response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    chain.append(reply)
    await message.answer(reply)


#Learn
@router.callback_query(F.data == 'chain_find', StateFilter(default_state))
async def chain_find(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f"Вы выбрали режим 'Практика' в игре 'Предожение'")
    await callback.message.answer(text=f"Напишите слово")
    await state.set_state(Gen.chain_learn)

@router.message(StateFilter(Gen.chain_learn), (F.text & F.text != '/stop'))
async def chain_find(message: Message, state: FSMContext):
    input = message.text 
    res = await chain_learn(input)
    await message.answer(res)
#-----------------------------------------------------------------------------------------------







#Adj-----------------------------------------------------------------------------------------------
@router.message(Command(commands='adjectives'), StateFilter(default_state))
async def choice_adj(message: Message):
    await message.answer(text=LEX['adjective'], reply_markup=kb.adj_menu)


#Play    
@router.callback_query(F.data == 'adj_play', StateFilter(default_state))
async def adj_play(callback: CallbackQuery, state: FSMContext):
    global first_adj, second_adj
    first_adj = adjectives.sample().values[0][0]
    second_adj = adjectives.sample().values[0][0]
    await callback.message.answer(text=f"Вы выбрали режим 'Игра' в игре 'Два прилагательных'")
    await callback.message.answer(text=f"Прилагательные:\n{first_adj}, {second_adj}")
    await state.set_state(Gen.adj_play)


@router.message(StateFilter(Gen.adj_play), (F.text & F.text != '/stop'))
async def adj_play(message: Message, state: FSMContext):
    global first_adj, second_adj
    f = first_adj
    s = second_adj
    messages = [
        {"role": "system", "content": "Ты - нейросеть, которая помогает развивать навыки коммуникации."},
        {"role": "user", "content": f'Есть два прилагательных: {f} и {s}. С какими существительными у тебя ассоциируется это описание? Напиши таких 5 существительных '}
    ]
    response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages)
    reply = response["choices"][0]["message"]["content"]
    await message.answer(reply)
    first_adj = adjectives.sample().values[0][0]
    second_adj = adjectives.sample().values[0][0]
    await message.answer(text=f"Прилагательные:\n{first_adj}, {second_adj}")
#-------------------------------------------------------------------------------------------------



# Этот хэндлер будет срабатывать на команду "/stop" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='stop'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из игры'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()