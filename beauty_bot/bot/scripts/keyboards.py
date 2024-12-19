from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📝  Записаться через салон  ", callback_data="salon")],
        [InlineKeyboardButton("🖊️  Записаться через мастера", callback_data="master")],
        [InlineKeyboardButton("📞 Позвонить администратору", callback_data="call_admin")],

    ]
    return InlineKeyboardMarkup(keyboard)


def get_master_keyboard():
    keyboard = [
        [InlineKeyboardButton("‍👩‍🔧 Ольга Смирнова ", callback_data="master_1")],
        [InlineKeyboardButton("👩‍🔧 Надежда Литвина ", callback_data="master_2")],
        [InlineKeyboardButton("👩‍🔧 Лариса Новикова ", callback_data="master_3")],
        [InlineKeyboardButton("👩‍🔧 Светлана Ларина", callback_data="master_4")],
        [InlineKeyboardButton("👩‍🔧 Любовь Макеева", callback_data="master_5")],
        [InlineKeyboardButton("👩‍🔧 Татьяна Смелова", callback_data="master_6")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_date_keyboard():
    keyboard = [
        [InlineKeyboardButton("📅 1 октября", callback_data="date_2023-10-01"),
         InlineKeyboardButton("📅 3 октября", callback_data="date_2023-10-03"),
         InlineKeyboardButton("📅 4 октября", callback_data="date_2023-10-04")],
        [InlineKeyboardButton("📅 6 октября", callback_data="date_2023-10-06"),
         InlineKeyboardButton("📅 8 октября", callback_data="date_2023-10-08"),
         InlineKeyboardButton("🔙 Назад", callback_data="choose_procedure")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_salon_keyboard():
    keyboard = [
        [InlineKeyboardButton("‍🏠 Салон 'Челка' ", callback_data="salon_1"),
         InlineKeyboardButton("🏠 Салон 'Стиляга' ", callback_data="salon_2"),
         InlineKeyboardButton("🏠 Салон 'Гармония' ", callback_data="salon_3")],
        [InlineKeyboardButton("🏠 Салон 'Элеганс' ", callback_data="salon_4"),
         InlineKeyboardButton("🏠 Салон 'Краса' ", callback_data="salon_5"),
         InlineKeyboardButton("🏠 Салон 'Стиль' ", callback_data="salon_6")]

    ]
    return InlineKeyboardMarkup(keyboard)


def get_procedure_keyboard():
    keyboard = [
        [InlineKeyboardButton("✂️ Стрижка", callback_data="procedure_cut"),
         InlineKeyboardButton("💅 Маникюр", callback_data="procedure_manicure"),
         InlineKeyboardButton("🦶 Педикюр", callback_data="procedure_pedicure")],
        [InlineKeyboardButton("🌸 Уход за лицом", callback_data="procedure_facial"),
         InlineKeyboardButton("🕊️ Эпиляция", callback_data="procedure_waxing"),
         InlineKeyboardButton("🕊💆 Массаж", callback_data="procedure_massage")],
        [InlineKeyboardButton("🎨 Окрашивание волос", callback_data="procedure_color"),
         InlineKeyboardButton("🔙 Назад", callback_data="salon")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_time_slots_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏳ 9:00", callback_data="time_9:00"),
         InlineKeyboardButton("⏳ 11:00", callback_data="time_11:00"),
         InlineKeyboardButton("⏳ 13:00", callback_data="time_13:00")],
        [InlineKeyboardButton("⏳ 15:00", callback_data="time_15:00"),
         InlineKeyboardButton("⏳ 16:00", callback_data="time_16:00"),
         InlineKeyboardButton("⏳ 18:00", callback_data="time_18:00")],
        [InlineKeyboardButton("🔙 Назад", callback_data="choose_procedure")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_confirm_keyboard():
    keyboard = [
        [InlineKeyboardButton("Подтвердить запись", callback_data="confirm_booking")]
    ]
    return InlineKeyboardMarkup(keyboard)
