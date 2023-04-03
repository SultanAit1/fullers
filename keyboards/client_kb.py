from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from aiogram.types import InlineKeyboardButton, CallbackQuery



from aiogram import  Dispatcher, types

start_markup = InlineKeyboardMarkup(row_width=6, sizex=2)

one = InlineKeyboardButton(text='ERSAG компания жөнундө✅', callback_data="one")
three = InlineKeyboardButton(text='ERSAG Продукция🌿', callback_data='three')
two = InlineKeyboardButton(text='Маркетинг планы💹', callback_data='two')
four = InlineKeyboardButton(text='Команда жогорулатуу жөнундө✳', callback_data='four')
five = InlineKeyboardButton(text='ERSAG менен иштөө❇', callback_data='five')
last = InlineKeyboardButton(text='Бот заказ берү️', callback_data='last', url="https://t.me/Demonstrationsbot")
start_markup.add(one, )
start_markup.add(three,two)
start_markup.add(five)
start_markup.add(four)

start_markup.add(last)



main_markup = InlineKeyboardMarkup(row_width=1)
exit_1 = InlineKeyboardButton(text="🔹Башкы меню🔹", callback_data='exit_1')
main_markup.add(exit_1)


url_markup = InlineKeyboardMarkup(row_width=5)
kyrg = InlineKeyboardButton(text='Каталог: Кыргызстан 🇰🇬 ', callback_data='kyrg', url='https://goo.su/ZZu4dty')
russia = InlineKeyboardButton(text='Каталог: Казахстан 🇰🇿 ', callback_data='russia', url='https://goo.su/uM5a2pT')
kazax = InlineKeyboardButton(text='Каталог: Узбекистан 🇺🇿 ', callback_data='kazax', url="https://goo.su/lAzUR4B")
uzb = InlineKeyboardButton(text='Каталог: Россия  🇷🇺 ', callback_data='uzb',url="https://goo.su/lqwJz3")
url_markup.add(kyrg
)
url_markup.add(russia)
url_markup.add(kazax)
url_markup.add(uzb)
url_markup.add(exit_1)

