from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    
)

inline_keyboard1 = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "Шины", callback_data="tires", color="primary")],
                       [InlineKeyboardButton(text = "Диски", callback_data="disks", color="danger")],
                        [InlineKeyboardButton(text = "Лобовое стекло", callback_data="window", color="success")],
    ]
)

inline_keyboard2 = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = "Вернуться назад", callback_data="back")]]
)

reply_keyboard = ReplyKeyboardMarkup(
    keyboard = [[KeyboardButton(text = "Вернуться в главное меню")]],
                      resize_keyboard=True
                      )

