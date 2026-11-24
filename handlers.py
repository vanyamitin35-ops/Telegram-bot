from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from config import PAYMENT_TOKEN, ADMIN_ID
import keyboads as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import sql
from datetime import datetime

router = Router()

class InputFeedback(StatesGroup):
    waiting_feedback = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "👋 Привет! Этот бот сделан для покупки услуг из дома!\n\n"
        "🚗 Посмотреть меню товаров на авто: /avto\n"
        "🔎 Информация про наш магазин: /info\n"
        "📥 Для просмотра корзины: /cart\n"
        "✅ Чтобы подтвердить заказ: /confirm\n"
        "🔎 Помощь по командам: /help\n"
    )
    await message.answer(text)
    
    
@router.message(Command("avto"))
async def avto_cmd(message: Message):
    text = (
        "🚗 Выберите товары:\n"
        " Шины: 1500 рублей\n"
        " Диски на колёса: 2000 рублей\n"
        "🚗 Лобовое стекло: 5000 рублей\n"
    )
        
    await message.answer(text,
        reply_markup=kb.inline_keyboard1
    )
    
    
@router.message(Command("info"))
async def info_cmd(message: Message):
    await message.answer("👋 Это тестовый бот)",
                         reply_markup=kb.inline_keyboard2)
    
@router.message(Command("help"))
async def help_cmd(message: Message):
    text = (
        "🔎 Все команды в боте\n"
        "/avto - Меню товаров для авто\n"
        "/back - Вернуться на главное меню\n"
        "/info - Информация про магазин\n"
        "/cart - Просмотр корзины\n"
        "/confirm - Подтверждение заказа\n"
        "/help - Помощь по командам\n"
        "/admin_cmd - Команды админки (Для администраторов)\n"
    )
    await message.answer(text, reply_markup=kb.inline_keyboard2)
    
@router.message(Command("admin_cmd"))
async def admin_cmd(message: Message):
    text = (
        "🔎 Команды для админов\n"
        "/admin - Вход в админку\n"
        "admin_feedbacks - Просмотр отзывов\n"
        "admin_orders - Просмотр покупок\n"
    )
    await message.answer(text, reply_markup=kb.inline_keyboard2)
    
@router.message(Command("back"))
async def back_cmd(message: Message):
    text = (
        "👋 Привет! Этот бот сделан для покупки услуг из дома!\n\n"
        "🚗 Посмотреть меню товаров на авто: /avto\n"
        "🔎 Информация про наш магазин: /info\n"
        "📥 Для просмотра корзины: /cart\n"
        "✅ Чтобы подтвердить заказ: /confirm\n"
        "🔎 Помощь по командам: /help\n"
    )
    await message.answer(text)


@router.message(F.text == "Вернуться в главное меню")
async def back_cmd(message: Message):
    text = (
        "👋 Привет! Этот бот сделан для покупки услуг из дома!\n\n"
        "🚗 Посмотреть меню товаров на авто: /avto\n"
        "🔎 Информация про наш магазин: /info\n"
        "📥 Для просмотра корзины: /cart\n"
        "✅ Чтобы подтвердить заказ: /confirm\n"
        "🔎 Помощь по командам: /help\n"
    )
    await message.answer(text)
    
@router.callback_query(F.data == "back")
async def call_back_cmd(call: CallbackQuery):
    text = (
        "👋 Привет! Этот бот сделан для покупки услуг из дома!\n\n"
        "🚗 Посмотреть меню товаров на авто: /avto\n"
        "🔎 Информация про наш магазин: /info\n"
        "📥 Для просмотра корзины: /cart\n"
        "✅ Чтобы подтвердить заказ: /confirm\n"
        "🔎 Помощь по командам: /help\n"
    )
    await call.message.answer(text)
    await call.answer()
        
    
    
@router.callback_query(F.data == "tires")
async def call_tires(call: CallbackQuery):
    db_session = None # Инициализируем db_session как None на случай, если возникнет ошибка до его получения
    try:
        # Мы используем next() для получения сессии, а затем явно закрываем ее в finally.
        db_session = next(sql.get_db())
        
        new_orders2 = sql.Orders(
            user_id=call.from_user.id,
            name="Шины",
            price=1500, 
        )
        
        db_session.add(new_orders2)

        db_session.commit()
                
        await call.message.answer("✅ Товар добавлен в корзину",
                                  "/cart - 🛒Корзина")
        await call.answer() 
        
    except sql.SQLAlchemyError as e: 
        # Откатываем транзакцию в случае ошибки базы данных
        if db_session:
            db_session.rollback()
        print(f"Произошла ошибка базы данных при добавлении заказа: {e}")
        await call.message.answer("❌ Произошла ошибка при добавлении товара в корзину.")
        await call.answer("Произошла ошибка при работе с базой данных.", show_alert=True)
    except Exception as e:
        # Откатываем транзакцию в случае любой другой ошибки (если db_session уже была получена)
        if db_session:
            db_session.rollback()
        print(f"Произошла непредвиденная ошибка: {e}")
        await call.message.answer("❌ Произошла непредвиденная ошибка при добавлении товара.")
        await call.answer("Произошла непредвиденная ошибка.", show_alert=True)
    finally:
        # Гарантируем закрытие сессии базы данных
        if db_session:
            db_session.close()
        
@router.callback_query(F.data == "disks")
async def call_disks(call: CallbackQuery):
    db_session = None # Инициализируем db_session как None на случай, если возникнет ошибка до его получения
    try:
        # Мы используем next() для получения сессии, а затем явно закрываем ее в finally.
        db_session = next(sql.get_db())
        
        new_orders2 = sql.Orders(
            user_id=call.from_user.id,
            name="Диски",
            price=2000, 
        )
        
        db_session.add(new_orders2)
        
        db_session.commit()
                
        await call.message.answer("✅ Товар добавлен в корзину",
                                  '/cart - 🛒Корзина')
        await call.answer() 
        
    except sql.SQLAlchemyError as e: 
        # Откатываем транзакцию в случае ошибки базы данных
        if db_session:
            db_session.rollback()
        print(f"Произошла ошибка базы данных при добавлении заказа: {e}")
        await call.message.answer("❌ Произошла ошибка при добавлении товара в корзину.")
        await call.answer("Произошла ошибка при работе с базой данных.", show_alert=True)
    except Exception as e:
        # Откатываем транзакцию в случае любой другой ошибки (если db_session уже была получена)
        if db_session:
            db_session.rollback()
        print(f"Произошла непредвиденная ошибка: {e}")
        await call.message.answer("❌ Произошла непредвиденная ошибка при добавлении товара.")
        await call.answer("Произошла непредвиденная ошибка.", show_alert=True)
    finally:
        # Гарантируем закрытие сессии базы данных
        if db_session:
            db_session.close()
        
        
@router.callback_query(F.data == "window")
async def call_window(call: CallbackQuery):
    db_session = None # Инициализируем db_session как None на случай, если возникнет ошибка до его получения
    try:
        db_session = next(sql.get_db())
        
        new_orders2 = sql.Orders(
            user_id=call.from_user.id,
            name="Лобовое стекло",
            
            price=5000, 
        )
        
        db_session.add(new_orders2)
        
        db_session.commit()
                
        await call.message.answer("✅ Товар добавлен в корзину",
                                  "/cart - 🛒Корзина")
        
        await call.answer() 
        
    except sql.SQLAlchemyError as e: 
        # откат транзакции в случае ошибки бд
        if db_session:
            db_session.rollback()
        print(f"Произошла ошибка базы данных при добавлении заказа: {e}")
        await call.message.answer("❌ Произошла ошибка при добавлении товара в корзину.")
        await call.answer("Произошла ошибка при работе с базой данных.", show_alert=True)
    except Exception as e:
        # Откатываем транзакцию в случае любой другой ошибки (если db_session уже была получена)
        if db_session:
            db_session.rollback()
        print(f"Произошла непредвиденная ошибка: {e}")
        await call.message.answer("❌ Произошла непредвиденная ошибка при добавлении товара.")
        await call.answer("Произошла непредвиденная ошибка.", show_alert=True)
    finally:
        # ✅ ИСПРАВЛЕНИЕ 5: Гарантируем закрытие сессии базы данных
        if db_session:
            db_session.close()
            
            
@router.message(Command("cart"))
async def cart_cmd(message: Message):
    db_session = None
    try:
        db_session = next(sql.get_db())
        user_orders = db_session.query(sql.Orders).filter(sql.Orders.user_id == message.from_user.id).all()
        
        if not user_orders:
            await message.answer("🛒 Ваша корзина пуста.")
            return
        
        cart_text = "🛒 Ваша корзина:\n\n"
        total_price = 0
        
        for order in user_orders:
            cart_text += f"📦 {order.name} - {order.price} руб.\n"
            total_price += order.price
        
        cart_text += f"\n💰 Общая стоимость: {total_price} руб."
        
        await message.answer(cart_text,
                             "/confirm - Подтвердить заказы",
                             reply_markup=kb.reply_keyboard)
        
    except sql.SQLAlchemyError as e:
        print(f"Произошла ошибка базы данных при получении корзины: {e}")
        await message.answer("❌ Произошла ошибка при загрузке вашей корзины.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        await message.answer("❌ Произошла непредвиденная ошибка при загрузке вашей корзины.")
    finally:
        if db_session:
            db_session.close()
            
@router.message(Command("delete"))
async def delete_cmd(message: Message):
    db_session = None
    try:
        db_session = next(sql.get_db())
        user_orders = db_session.query(sql.Orders).filter(sql.Orders.user_id == message.from_user.id).all()
        
        if not user_orders:
            await message.answer("🛒 Ваша корзина уже пуста.")
            return
        
        for order in user_orders:
            db_session.delete(order)
            
        deleted_orders = sql.deleted_orders(
            user_id = message.from_user.id,
            deleted_orders = sql.Orders.name,
        )
        
        db_session.add(deleted_orders)
            
        
        db_session.commit()
        
        await message.answer("🗑️ Ваша корзина была очищена.")
        
    except sql.SQLAlchemyError as e:
        if db_session:
            db_session.rollback()
        print(f"Произошла ошибка базы данных при удалении корзины: {e}")
        await message.answer("❌ Произошла ошибка при очистке вашей корзины.")
    except Exception as e:
        if db_session:
            db_session.rollback()
        print(f"Произошла непредвиденная ошибка: {e}")
        await message.answer("❌ Произошла непредвиденная ошибка при очистке вашей корзины.")
    finally:
        if db_session:
            db_session.close()
            
            
@router.message(Command("confirm"))
async def confirm_cmd(message: Message):
    db_session = None
    try:
        db_session = next(sql.get_db())
        
        user_orders = db_session.query(sql.Orders).filter(sql.Orders.user_id == message.from_user.id).all()
        
        if not user_orders:
            await message.answer("🛒 Ваша корзина пуста. Добавьте товары перед подтверждением заказа.")
            return

        # Подготавливаем товары для инвойса
        prices = []
        total_amount_kopecks = 0 # Сумма в копейках (или центах)
        order_description_items = []

        for order in user_orders:
            # LabeledPrice принимает сумму в копейках/центах
            prices.append(LabeledPrice(label=order.name*100, amount=order.price*100)) # order.price уже в копейках/центах
            total_amount_kopecks += order.price
            order_description_items.append(f"{order.name} ({order.price/100:.2f} RUB)") # Для описания

        order_description = "Ваш заказ:\n" + "\n".join(order_description_items) + f"\nВсего: {total_amount_kopecks/100:.2f} RUB"
        
        
        
        # Отправляем инвойс
        # payload можно использовать для привязки платежа к конкретному пользователю или заказу
        await message.bot.send_invoice(
            chat_id=message.chat.id,
            title="Подтверждение заказа",
            description=order_description,
            payload=f"user_{message.from_user.id}_order_{datetime.now().timestamp()}", # Уникальный идентификатор заказа
            provider_token=PAYMENT_TOKEN,
            currency="RUB", # Валюта
            prices=prices,
            max_tip_amount=500000, # Максимальная сумма чаевых (в копейках)
            suggested_tip_amounts=[1000, 2000, 5000], # Предлагаемые суммы чаевых
            start_parameter="confirm_order", # Необязательный параметр для глубоких ссылок
            provider_data=None, # Дополнительные данные для платежного провайдера (если нужно)
        )
        
    except sql.SQLAlchemyError as e:
        if db_session:
            db_session.rollback()
        print(f"Произошла ошибка базы данных при подготовке заказа к оплате: {e}")
        await message.answer("❌ Произошла ошибка при подготовке вашего заказа к оплате.")
    except Exception as e:
        if db_session:
            db_session.rollback()
        print(f"Произошла непредвиденная ошибка при подготовке заказа к оплате: {e}")
        await message.answer("❌ Произошла непредвиденная ошибка при подготовке вашего заказа к оплате.")
    finally:
        if db_session:
            db_session.close()

# обработчик для pre_checkout_query (перед оплатой)
@router.pre_checkout_query()
async def pre_checkout_check(pre_checkout_query: PreCheckoutQuery):
    # Здесь можно выполнить дополнительные проверки, например,
    # убедиться, что товары еще есть в наличии, или что сумма корректна.
    print(f"Получен pre_checkout_query от {pre_checkout_query.from_user.id}: {pre_checkout_query.total_amount}")

    await pre_checkout_query.answer(ok=True)
    
# обработчик для successful_payment (после успешной оплаты)
@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    db_session = None
    try:
        db_session = next(sql.get_db())
        
        user_id = message.from_user.id
        
        # Получаем все текущие заказы пользователя из корзины
        user_orders_in_cart = db_session.query(sql.Orders).filter(sql.Orders.user_id == user_id).all()
        
        if not user_orders_in_cart:
            # если payment_payload не привязан к user_id и order_id в бд.
            # Для надежности можно попытаться восстановить заказ по payload, если это возможно.
            await message.answer("❌ Не удалось найти ваши заказы для подтверждения, но платеж прошел.")
            print(f"Ошибка: Платеж для {user_id} прошел, но заказов в корзине не найдено.")
            return

        # Перемещаем товары из Orders в Confirmed_Orders
        for order in user_orders_in_cart:
            new_confirmed_order = sql.Confirmed_Orders(
                order_id=order.id, # Ссылка на оригинальный ID заказа
                user_id=order.user_id,
                name=order.name,
                price=order.price,
                time=datetime.utcnow() # Время подтверждения
            )
            db_session.add(new_confirmed_order)
            # Удаляем оригинальный заказ из корзины
            db_session.delete(order)
            
        db_session.commit()
        
        await message.answer("✅ Ваш заказ успешно оплачен и подтвержден! Спасибо за покупку.",
                            "Напишите про нас отзыв пожалуйста - /feedback") 
        
    except sql.SQLAlchemyError as e:
        if db_session:
            db_session.rollback()
        print(f"Произошла ошибка базы данных при обработке успешного платежа: {e}")
        await message.answer("❌ Произошла ошибка при сохранении вашего подтвержденного заказа.")
    except Exception as e:
        if db_session:
            db_session.rollback()
        print(f"Произошла непредвиденная ошибка при обработке успешного платежа: {e}")
        await message.answer("❌ Произошла непредвиденная ошибка при обработке вашего подтвержденного заказа.")
    finally:
        if db_session:
            db_session.close()
            
            
@router.message(Command("feedback"))
async def feedback_cmd(message: Message, state: FSMContext):
    await message.answer("🤗 Напишите что-то про нас")
    await state.set_state(InputFeedback.waiting_feedback)

@router.message(InputFeedback.waiting_feedback)
async def feedback_cmd(message: Message, state: FSMContext):
    db_session = None
    try:
        db_session = next(sql.get_db())
        
        feedback_sql = db_session.query(sql.feedbacks).filter(sql.feedbacks.user_id == message.from_user.id).first()
        
        for feedback in feedback_sql:
            new_feedback = sql.feedbacks(
                user_id=message.from_user.id,
                feedback=int(message.text),
                time = datetime.utcnow()
                )
        
        db_session.add(new_feedback)
        db_session.commit()
        await state.clear()
        
        await message.answer("Спасибо за ваш отзыв!")
        
    except sql.SQLAlchemyError as e:
        if db_session:
            db_session.rollback()
        print(f"Произошла ошибка базы данных при сохранении отзыва: {e}")
        await message.answer("❌ Произошла ошибка при сохранении вашего отзыва.")
    except Exception as e:
        if db_session:
            db_session.rollback()
        print(f"Произошла непредвиденная ошибка при сохранении отзыва: {e}")
        await message.answer("❌ Произошла непредвиденная ошибка при сохранении вашего отзыва.")
    finally:
        if db_session:
            db_session.close()
            
    await state.clear()
    

@router.message(Command("history_orders"))
async def history_orders_cmd(message: Message):
    db_session = None
    try:
        dp_session = next(sql.get_db)
        
        history_orders = dp_session.query(sql.Confirmed_Orders).filter(sql.Confirmed_Orders.user_id == message.from_user.id).all()
        
        if not history_orders:
            await message.answer("📭 У вас нет истории заказов.")
            return
        
        text = "📋 Ваша история заказов:\n\n"
        for order in history_orders:
            text += f"📦 Название: {order.name} - Цена: {order.price} руб. Дата: {order.time}\n"
        
        await message.answer(text)
    
    except sql.SQLAlchemyError as e:
        print(f"Произошла ошибка базы данных при получении истории заказов: {e}")
        await message.answer("❌ Произошла ошибка при получении вашей истории заказов.")
    finally:
        if db_session:
            db_session.close()

# админка

@router.message(Command("admin"))
async def admin_cmd(message: Message):
    if message.from_user.id == ADMIN_ID: 
        text = (
            "🔎 Команды для админов\n"
            "/admin - Вход в админку\n"
            "/admin_feedbacks - Просмотр отзывов\n"
            "/admin_orders - Просмотр покупок\n"
            "/admin_del_orders = Просмотр удаленных заказов\n"
        )
        await message.answer(text, reply_markup=kb.inline_keyboard2)
        
    else:
        await message.answer("❌ У вас нет доступа к админке.")
        
@router.message(Command("admin_feedbacks"))
async def admin_feedbacks_cmd(message: Message):
    if message.from_user.id == ADMIN_ID:
        feedbacks = sql.get_all_feedbacks()
        if not feedbacks:
            await message.answer("📭 Нет отзывов.")
        else:
            feedbacks_text = "📋 Все отзывы:\n\n"
            for feedback in feedbacks:
                feedbacks_text += f"👤 Пользователь ID: {feedback.user_id}\n💬 Отзыв: {feedback.feedback}\n🕒 Время: {feedback.time}\n\n"
            await message.answer(feedbacks_text)
    else:
        await message.answer("У вас нет прав доступа")
        
@router.message(Command("admin_orders"))
async def admin_orders_cmd(message: Message):
    if message.from_user.id == ADMIN_ID:
        confirmed_orders = sql.get_all_confirmed_orders()
        if not confirmed_orders:
            await message.answer("📭 Нет подтвержденных заказов.")
    
        confirmed_orders_text = "📋 Все подтвержденные заказы:\n\n"
        for order in confirmed_orders:
            confirmed_orders_text += f"👤 Пользователь ID: {order.user_id}\n📦 Заказ: {order.order}\n🕒 Цена: {order.price}\n 🕒 Время: {order.time}\n\n"
        await message.answer(confirmed_orders_text)
    else:
        await message.answer("У вас нет прав доступа")
            
    
@router.message(Command("admin_del_orders"))
async def admin_del_orders(message: Message):
    if message.from_user.id == ADMIN_ID:
        deleted_orders2 = sql.get_all_deleted_orders()
        
        if not deleted_orders2:
            await message.answer("📭 Нету удаленных заказов")
        else:
        
            deleted_orders_text = "📋 Все удаленные заказы:\n\n"
        
            for deleted_order in deleted_orders2:
            
                deleted_orders_text += f"👤 Пользователь ID: {deleted_order.user_id}\n📦 Заказ: {deleted_order.order}\n🕒"
                await message.answer(deleted_orders_text)
    else:
                await message.answer("У вас нет прав доступа")