import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from urfu_parser_v2 import UrfuParser

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "7817389200:AAHUWxCcW2aWIHYxaGLy1mKdi6tiq9NxRPU"

# Создаем экземпляр парсера
parser = UrfuParser()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_message = """
🎓 **Добро пожаловать в бот УрФУ!**

Этот бот поможет вам получить информацию о вступительных испытаниях по ID абитуриента.

📝 **Как пользоваться:**
• Просто отправьте мне ID абитуриента (7-значное число)
• Я найду и покажу всю информацию о вступительных испытаниях

🔍 **Пример:** 4475115

❓ **Команды:**
/start - показать это сообщение
/help - помощь

Отправьте ID абитуриента, чтобы начать поиск! 🚀
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_message = """
🆘 **Помощь по использованию бота**

📋 **Что делает бот:**
Бот парсит информацию о вступительных испытаниях с официального сайта УрФУ по ID абитуриента.

🔍 **Как найти ID абитуриента:**
1. Зайдите на сайт УрФУ в раздел "Списки поступающих"
2. ID абитуриента - это 7-значное число
3. Пример: 4475115

📝 **Что показывает бот:**
• Направление подготовки
• Образовательную программу
• Институт
• Форму обучения
• Тип конкурса
• Статус участия
• Приоритет
• Общий балл
• Детальную информацию о вступительных испытаниях

⚠️ **Важно:**
• ID должен состоять из цифр
• Длина ID обычно 7 цифр
• Если абитуриент не найден, проверьте правильность ID

🔄 **Попробуйте снова:**
Просто отправьте ID абитуриента числом.
    """
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    user_message = update.message.text.strip()
    
    # Проверяем, что сообщение содержит только цифры
    if not user_message.isdigit():
        await update.message.reply_text(
            "❌ Пожалуйста, отправьте только ID абитуриента (числовое значение).\n"
            "Пример: 4475115"
        )
        return
    
    # Проверяем длину ID
    if len(user_message) < 6 or len(user_message) > 8:
        await update.message.reply_text(
            "❌ ID абитуриента должен содержать 6-8 цифр.\n"
            "Пример: 4475115"
        )
        return
    
    # Отправляем сообщение о начале поиска
    search_message = await update.message.reply_text(
        f"🔍 Ищу информацию для ID: {user_message}...\n"
        "⏳ Пожалуйста, подождите..."
    )
    
    try:
        # Выполняем поиск
        result = parser.search_by_id(user_message)
        
        # Форматируем результат
        if result.get('success'):
            formatted_result = parser.format_result_for_telegram(result)
            
            # Telegram имеет лимит на длину сообщения (4096 символов)
            if len(formatted_result) > 4000:
                # Разбиваем длинное сообщение на части
                parts = []
                current_part = ""
                lines = formatted_result.split('\n')
                
                for line in lines:
                    if len(current_part + line + '\n') > 4000:
                        if current_part:
                            parts.append(current_part)
                        current_part = line + '\n'
                    else:
                        current_part += line + '\n'
                
                if current_part:
                    parts.append(current_part)
                
                # Удаляем сообщение о поиске
                await search_message.delete()
                
                # Отправляем части по очереди
                for i, part in enumerate(parts, 1):
                    if i == 1:
                        await update.message.reply_text(part, parse_mode='Markdown')
                    else:
                        await update.message.reply_text(f"**Продолжение ({i}):**\n\n{part}", parse_mode='Markdown')
            else:
                # Обновляем сообщение с результатом
                await search_message.edit_text(formatted_result, parse_mode='Markdown')
        else:
            # Обновляем сообщение с ошибкой
            await search_message.edit_text(
                f"❌ {result.get('error', 'Неизвестная ошибка')}\n\n"
                "💡 Проверьте правильность ID и попробуйте снова."
            )
    
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {e}")
        await search_message.edit_text(
            "❌ Произошла ошибка при получении данных.\n"
            "🔄 Попробуйте позже или проверьте ID."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Основная функция запуска бота"""
    print("🤖 Запуск Telegram-бота УрФУ...")
    print(f"🔑 Токен: {BOT_TOKEN[:10]}...")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    print("✅ Бот настроен и готов к работе!")
    print("📱 Отправьте /start в Telegram для начала работы")
    print("🛑 Нажмите Ctrl+C для остановки")
    
    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

