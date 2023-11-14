from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    img_learn = State()
    img_train = State()

    audio_play = State()
    
    sent_learn = State()
    sent_train = State()

    chain_play = State()
    chain_learn = State()

    adj_play = State()