#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой скрипт запуска Telegram-бота УрФУ
"""

import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("🎓 TELEGRAM-БОТ УрФУ - ПАРСЕР ВСТУПИТЕЛЬНЫХ ИСПЫТАНИЙ")
    print("=" * 60)
    print("📋 Описание: Бот для получения информации о вступительных")
    print("    испытаниях по ID абитуриента с сайта УрФУ")
    print("🔗 Сайт УрФУ: https://urfu.ru")
    print("=" * 60)
    print()
    
    # Проверяем наличие необходимых файлов
    required_files = ['telegram_bot.py', 'urfu_parser_v2.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ ОШИБКА: Отсутствуют необходимые файлы:")
        for file in missing_files:
            print(f"   - {file}")
        print()
        print("💡 Убедитесь, что все файлы находятся в одной папке с этим скриптом")
        input("Нажмите Enter для выхода...")
        return
    
    # Проверяем установку зависимостей
    try:
        import requests
        import telegram
        from bs4 import BeautifulSoup
        print("✅ Все зависимости установлены")
    except ImportError as e:
        print(f"❌ ОШИБКА: Не установлена зависимость: {e}")
        print()
        print("💡 Установите зависимости командой:")
        print("   pip install -r requirements.txt")
        print()
        print("📋 Или установите вручную:")
        print("   pip install requests python-telegram-bot beautifulsoup4")
        input("Нажмите Enter для выхода...")
        return
    
    print("🚀 Запуск бота...")
    print("📱 После запуска найдите бота в Telegram и отправьте /start")
    print("🛑 Для остановки нажмите Ctrl+C")
    print("=" * 60)
    print()
    
    try:
        # Запускаем основной скрипт бота
        subprocess.run([sys.executable, 'telegram_bot.py'])
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка при запуске: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == '__main__':
    main()
