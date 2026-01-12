from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import emoji

btn_info = KeyboardButton(f"{emoji.INFORMATION} Info")
btn_games = KeyboardButton(f"{emoji.ALIEN_MONSTER} Hry")
btn_generation = KeyboardButton(f"{emoji.PAINTBRUSH} Tvorba obrázků pomocí AI")
btn_rps = KeyboardButton(f"{emoji.ROCK} Kámen, nůžky, papír")
btn_quest = KeyboardButton(f"{emoji.OPEN_BOOK} Detektivní hra")
btn_back = KeyboardButton(f"{emoji.LEFT_ARROW} Zpět")
btn_rock = KeyboardButton(f"{emoji.ROCK} Kámen")
btn_paper = KeyboardButton(f"{emoji.NEWSPAPER} papír")
btn_scissors = KeyboardButton(f"{emoji.SCISSORS} nůžky")

kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [btn_info, btn_games ],
        [btn_generation]
    ],
    resize_keyboard=True
)
kb_games = ReplyKeyboardMarkup(
    keyboard = [
        [btn_rps, btn_quest, btn_back]
    ],
    resize_keyboard=True
)

kb_rps = ReplyKeyboardMarkup(
    keyboard=[
        [btn_rock, btn_paper, btn_scissors],
        [btn_back]
    ],
    resize_keyboard=True
)

inline_quest = InlineKeyboardButton("Začít příběh", callback_data= 'start_quest')
inline_kb_start_quest = InlineKeyboardMarkup([
    [inline_quest]
])

inline_kb_read_papers = InlineKeyboardMarkup([
    [InlineKeyboardButton("Prohlédnout si údaje", callback_data="read_papers")],
])

inline_kb_theather = InlineKeyboardMarkup([
    [InlineKeyboardButton("Vyrazit do divadla", callback_data="theather")],
])

inline_kb_talk = InlineKeyboardMarkup([
    [InlineKeyboardButton("Promluvit si s Honori", callback_data="talk")],
])

inline_kb_question = InlineKeyboardMarkup([
    [InlineKeyboardButton("Zeptat se na Esther Elliot", callback_data="ask_about_Esther")],
    [InlineKeyboardButton("Vrátit se k prohlídce těla", callback_data="look_body")]
])

inline_kb_look_body = InlineKeyboardMarkup([
    [InlineKeyboardButton("Vrátit se k prohlídce těla", callback_data="look_body")],
])

inline_kb_ask = InlineKeyboardMarkup([
    [InlineKeyboardButton("Zeptat se zaměstnance na místa", callback_data="ask")],
])

inline_kb_alibi = InlineKeyboardMarkup([
    [InlineKeyboardButton("Vyslechnout Lionela de Curie", callback_data="go_Curie")],
    [InlineKeyboardButton("Vyslechnout Stefana Elliota", callback_data="go_Elliot")]
])

inline_kb_L_guilty = InlineKeyboardMarkup([
    [InlineKeyboardButton("Lionel de Curie – Vinen", callback_data="Curie_guilty")],
    [InlineKeyboardButton("Vyslechnout Stefana Elliota", callback_data="go_Elliot")]
])

inline_kb_Look_house = InlineKeyboardMarkup([
    [InlineKeyboardButton("Prohlédnout místnost", callback_data="Look_house")],
])

inline_kb_look_camera = InlineKeyboardMarkup([
    [InlineKeyboardButton("Prohlédnout záznamy z kamery", callback_data="look_camera")]
])

inline_kb_Elliot_guilty = InlineKeyboardMarkup([
    [InlineKeyboardButton("Stefan Elliot – Vinen", callback_data="Elliot_guilty")]
])