
from aiogram.types import InlineKeyboardButton, CallbackQuery
from config import bot, dp
from keyboards.client_kb import start_markup, main_markup, url_markup
import sqlite3
from aiogram import  Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_start = State()



conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS users
                (user_id INTEGER PRIMARY KEY)
                """)
conn.commit()


# noinspection SqlResolve
@dp.message_handler(content_types=['voice'])
async def handle_voice(message: types.Message):

    if message.from_user.id != 661114436:
        return

    voice_id = message.voice.file_id
    try:
            # Отправляем фото всем подписчикам
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            await bot.send_voice(chat_id=user_id, voice=voice_id)
        await message.answer(f" аудио успешно отправлено ({len(rows)} подписчикам).")
    except Exception as e:
        print(f"Ошибка при отправке видео: {e}")

# noinspection SqlResolve
@dp.message_handler(content_types=['video_note'])
async def handle_note(message: types.Message):
    if message.from_user.id != 661114436:
        return
    video_note_id = message.video_note.file_id
    try:
            # Отправляем фото всем подписчикам
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            await bot.send_video_note(chat_id=user_id, video_note=video_note_id)
        await message.answer(f"Видео успешно отправлено ({len(rows)} подписчикам).")
    except Exception as e:
        print(f"Ошибка при отправке видео: {e}")

# noinspection SqlResolve
@dp.message_handler(content_types=['video'])
async def handle_video(message: types.Message):
    # Получаем идентификатор фото
    video_id = message.video.file_id
    try:
        # Отправляем фото всем подписчикам
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            await bot.send_video(chat_id=user_id, video=video_id,caption=message.caption[6:] )
        await message.answer(f"Видео успешно отправлено всем подписчикам ({len(rows)} человек).")
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")

# noinspection SqlResolve
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    # Получаем идентификатор фото
    photo_id = message.photo[-1].file_id
    try:
        # Отправляем фото всем подписчикам
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            await bot.send_photo(chat_id=user_id, photo=photo_id,caption=message.caption[6:] )
        await message.answer(f"Фото успешно отправлено всем подписчикам ({len(rows)} человек).")
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")

# noinspection SqlResolve,PyUnboundLocalVariable
@dp.message_handler(commands=['/spam'])
async def spam_commands(message: types.Message):

    if message.from_user.id != 661114436:

        await message.answer("Вы не являетесь администратором.")
        return

    try:
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            await bot.send_message(chat_id=user_id, text=message.text[6:])
        await message.answer(f"Сообщение успешно отправлено ({len(rows)} подписчикам).")

    except Exception as e:
        print(f"Ошибка при отправке сообщения для пользователя {rows}: {e}")


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    cursor.execute("INSERT OR REPLACE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

    await bot.send_message(chat_id=message.from_user.id, text='https://youtu.be/UCF1oebyXMQ\n')
    await bot.send_message(chat_id=message.from_user.id,
                                                             text=
                                                                  "\n*😍Бул жасалма интеллект элементтери бар "
                                                                  'автоматташтырылган системанын негизги менюсу\n '
                                                                  '\n🌏Жана бул жерден сиз ДҮЙНӨЛҮК '
                                                                  'аталыштагы компания ERSAG  '
                                                                  'жөнүндө БААРЫН биле аласыз -!\n'
                                                                  '\nМен дароо жетекчимдин байланыштарын калтырам\n'
                                                                  '\n@Pomoshnikersag\n '
                                                                  '\nэгер кандайдыр бир суроолоруңуз болсо, сиз менен'
                                                                  'ар дайым байланыша аласыз\n'
                                    
                                                                  '\n📍Сиз аны менен ар дайым байланышып,'
                                                                  ', бардык суроолорго жооп ала аласыз\n  '
                                                                  
                                                
                                                                  '\n💡Эми жөн гана баскычтарды колдонуңуз,  '
                                                                  'сизди эмне кызыктырса, мен баарын айтып берейин*\n '
                                                                  '\n⬇️⬇️⬇️\n'

                                                        
                                                                  
                        

                               ,
        reply_markup=start_markup,parse_mode='Markdown')


    await UserStates.waiting_for_start.set()
    await state.update_data(user_id=message.from_user.id, username=message.from_user.username)
    # отправляем уведомление администратору
    await bot.send_message(661114436,
                           f"Пользователь {message.from_user.id} (@{message.from_user.username}) начал использовать бота")


@dp.callback_query_handler(text="one")
async def one(callback: CallbackQuery):
    one = InlineKeyboardButton("one", callback_data="one")
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id ,
   text='*♻Бүгүнкү күндө дүйнө жүзү боюнча миңдеген '
        'адамдар өздөрүнүн ден соолугуна жана '
        'айлана-чөйрөгө кам көрүшөт,'
        'ошондуктан алар 🔝ЭКО продукциясын тандап алышты!   '
        'Денизли шаарында негизделген жана Сапиндус жана  '
        'башка өсүмдүктөрдүн экстрактыларынын негизинде  '
        'табигый продукцияларды чыгарат\n '
        '\n❗20 жыл Эрсаг ийгиликтүү иштеп келет.\n'
        '\n🔔Продукциянын өндүрүш базалары Түркияда  '
        'жайгашкан жана 9 заводду камтыйт\n'
        '\n🔊Ар бири белгилүү бир продукцияларды '
        '(тазалоочу каражаттар, жуучу каражаттар, жеке гигиеналык каражаттар'
        'муздак пресстелген майлар жана косметикалык майлар, парфюмерияларды чыгарат.\n  '
        ''
        '\n🌿Эрсагдын бардык продукциялары органикалык,  '
        'курамында химиялык жана синтетикалык '
        'кошулмалар жана кошумчалар, өсүмдүк майлары, '
        'жыпар жыттуу заттар, парабендер, лаурилсульфаттар, фосфаттар, фтор жок.\n'
        '\n💯Компания 43 эл аралык продукцияны алган. анын продукциясына сертификаттар!\n'
        'HALAL , ECO CERT, ISO, GMP, OHRAS, BIO, ECO ж.б.*' ,reply_markup=main_markup, parse_mode='Markdown')




@dp.callback_query_handler(text="two")
async def two(callback: CallbackQuery):
    two = InlineKeyboardButton('two', callback_data='two')
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,
                                text="*📌ERSAG маркетинг планы - жана сиз үчүн дароо көптөгөн 'жакшылыктар': \n"
                                     "\n✅1. Компаниянын сайтында бекер катталуу жана"
                                     "биринчи заказдан 20% арзандатуу.  Ар бир буйрутма  "
                                     "менен сиз заказдын суммасына белек аласыз.\n"
                                     "\n✅2. Мансаптык арзандатуу өнөктөштүн баасына  "
                                     "кошулат, мансап канчалык жогору болсо, заказ"
                                     "боюнча жеке арзандатуу ошончолук чоң болот.  \n "
                                     "\n✅3. Туура карьера, сиз эч качан статустан ылдый "
                                     "түшпөйсүз.Бир жылда заказ кылсаңыз да.  \n"
                                     "\n✅4 Ай сайынгы активдүүлүк: же карьерасына "
                                     "жараша жеке көлөм же жаңы адамды биринчи сапка 2 "
                                     "упай тартиби менен кошуу.\n "
                                     "\n✅5. Эки айдын ичинде карьерасын жабуу мүмкүнчүлүгү. \n"
                                     "\n✅6. Упайларды мурунку айдан азыркыга которуу.  \n"
                                     "\n✅7. Айдын каалаган күнүндө карьера жана бир нече  "
                                     "карьера айына 10%дан 33%ке чейин жабуу мүмкүнчүлүгү. \n "
                                     "\n✅8. Бардык түзүм жана тереңдик боюнча төлөмдөр \n"
                                     "\n✅9. Лидерлик бонус  \n "
                                     "\n✅10. Маркетинг лидерлерин кескенге болбойт \n "
                                     "\n✅11. Картага ай сайын расмий бонустук төлөмдөр \n "
                                     "\n✅12. Эл аралык бизнес   \n"
                                     "\n✅13. Туулган кунго заказ бергенде компания кошумча белек берет\n* " , reply_markup=main_markup, parse_mode='Markdown'   )


@dp.callback_query_handler(text="three")
async def three(callback: CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id ,text="*🔋Компанияда товарлардын ассортименти абдан чоң, \n"
                                                                                                              "сиздерге ынгайлуу болушу \nүчүн мен бир нече\n"
                                                                                                              "каталогдорду тиркеп койдум,\n"
                                                                                                              "аларды карап көрө аласыздар.\n  "
                                                                                                              "\nЭгерде сиз жашаган өлкөңүз үчүн каталог керек  "
                                                                                                              "болсо, менин жетекчиме жазыныз\n"
                                                                                                              "\n✳️✳️✳️  "
                                                                                                              "\n@Pomoshnikersag \n"
                                                                                                              "\nбул маселе боюнча сизге жардам берет!* ",


                          reply_markup=url_markup,parse_mode='Markdown' )


@dp.callback_query_handler(text="last")
async def last(message: types.Message, ):
    last = InlineKeyboardButton('last', callback_data='last')
    await bot.send_message(chat_id=message.from_user.id, text="Хочу такого бота себе♻️")

@dp.callback_query_handler(text='four')
async def four(callback: CallbackQuery):
    four = InlineKeyboardButton('four', callback_data='four')
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id , text="🔔Биздин коомдогу промоушн системасы "
                                                                                                               "уникалдуу жана ал өзүнө төмөнкүлөрдү камтыйт:  \n "
                                                                                                 "\n✅ Кадамдык окутуу жана ар бир өнөктөштү колдоо, натыйжага алып келүү!  \n  "
                                                                                                 "\n✅ Эффективдүү системаларды, анын ичинде мен сыяктуу автоматташтырылган системаларды колдонуу)\n "
                                                                                                 "\n✅ Биздин ар бир өнөктөшүбүздө ушундай жардамчы бар жана сизге да жеткиликтүү болот!  \n "
                                                                                                 "\n✅ Жумуш үчүн даяр алгоритмдер, диалог скрипттери, эффективдүү инструменттер\n "
                                                                                                 "\n🤑 Онлайн режиминде да ишти айкалыштыруу - каалаган адамга ылайыктуу!  \n"
                                                                                                 "\n😎Баарыбыз бир күчтүү команда болуп баралы!  Ар бир адам үчүн - бул жакшы  перспективалар жана мүмкүнчүлүктөр! \n  "
                                                                                                 "\n⬇️   Көбүрөөк маалымат алуу үчүн негизги меню баскычын басыңыз! ",
                          reply_markup=main_markup, )

@dp.callback_query_handler(text='five')
async def five(callback: CallbackQuery):
    five = InlineKeyboardButton('five', callback_data='five')
    await bot.edit_message_text(chat_id=callback.message.chat.id ,message_id=callback.message.message_id, text="*😃Компаниянын өнөктөшү🤝 \nболуу үчүн менин жетекчиме \nжазыңыз.\nБул жерде анын байланыштары: "
                                                                                                               "\n✳️✳️✳️     \n"
                                                                                    
                                                                                                 "\n@Pomoshnikersag \n"
                                                                                                 "\nАл сизге туура катталып, компанияда сабаттуу баштоого жардам берет!\n"
                                                                                                 "\nЭгерде мен сизге дагы бир нерсе менен жардам бере алсам , "
                                                                                                 "анда негизги менюга  өтүңүз.  -  🤝\n"
                                                                                                 ""
                                                                                                 "\n💞Мен толугу менен сиздин кызматыңыздамын!*" ,reply_markup=main_markup, parse_mode='Markdown'   )


@dp.callback_query_handler(text="exit_1")
async def exit_1(callback: CallbackQuery):
    exit_1 = InlineKeyboardButton('exit_1', callback_data="exit_1")
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id, text=


    "\n*😍Бул жасалма интеллект элементтери бар "
    'автоматташтырылган системанын негизги менюсу\n '
    '\n🌏Жана бул жерден сиз ДҮЙНӨЛҮК '
    'аталыштагы компания ERSAG  '
    'жөнүндө БААРЫН биле аласыз -!\n'
    '\nМен дароо жетекчимдин байланыштарын калтырам\n'
    '\n@Pomoshnikersag\n '
    '\nэгер кандайдыр бир суроолоруңуз болсо, сиз менен'
    'ар дайым байланыша аласыз\n'

    '\n📍Сиз аны менен ар дайым байланышып,'
    ', бардык суроолорго жооп ала аласыз\n  '


    '\n💡Эми жөн гана баскычтарды колдонуңуз,  '
    'сизди эмне кызыктырса, мен баарын айтып берейин*\n '
    '\n⬇️⬇️⬇️\n',
                           reply_markup=start_markup, parse_mode='Markdown')




@dp.message_handler(commands=['follow'])
async def follow(message: types.Message):
    if message.from_user.id !=661114436:
        return
    cursor.execute('SELECT COUNT (user_id) FROM users')
    await bot.send_message(message.from_user.id, f'У вас {cursor.fetchone()[0]} подписчика')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(handle_note, commands=['note'])
    dp.register_message_handler(spam_commands, commands=['spam'])
    dp.register_message_handler(handle_voice, commands=['voice'])
    dp.register_message_handler(follow, commands=['follow'])
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(handle_video, commands=['spam'])
    dp.register_message_handler(handle_photo, commands=['spam'])
    dp.callback_query_handler(four, text='four')
    dp.callback_query_handler(five, text='five')
    dp.callback_query_handler(one, text='one')
    dp.callback_query_handler(two, text='two')
    dp.callback_query_handler(three, text='three')
    dp.callback_query_handler(last, text='last')
    dp.callback_query_handler(exit_1, text='exit_1')






