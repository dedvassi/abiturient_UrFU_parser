import requests
import json


class UrfuParser:
    def __init__(self):
        self.api_url = "https://urfu.ru/api/entrant/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def search_by_id(self, student_id):
        """
        Поиск информации о вступительных испытаниях по ID абитуриента через API
        """
        try:
            # Формируем параметры запроса к API
            params = {
                'page': 1,
                'size': 10,
                'search': str(student_id)
            }

            # Отправляем запрос к API
            response = self.session.get(self.api_url, params=params)

            if response.status_code != 200:
                return {"error": f"Ошибка API: {response.status_code}"}

            # Парсим JSON ответ
            data = response.json()

            if not data or 'items' not in data or len(data['items']) == 0:
                return {"error": "Абитуриент с указанным ID не найден"}

            # Извлекаем данные первого (и единственного) абитуриента
            entrant = data['items'][0]

            if 'applications' not in entrant or len(entrant['applications']) == 0:
                return {"error": "У абитуриента нет заявлений"}

            results = []

            # Обрабатываем все заявления абитуриента
            for application in entrant['applications']:
                # Извлекаем информацию о вступительных испытаниях
                exams_info = self.extract_exam_info_from_api(application.get('marks', {}))

                if exams_info:
                    result = {
                        "direction": application.get('speciality', ''),
                        "program": application.get('program', ''),
                        "institute": application.get('institute', ''),
                        "form": application.get('familirization', ''),
                        "competition": application.get('competition', ''),
                        "status": application.get('status', ''),
                        "priority": application.get('priority', ''),
                        "total_mark": application.get('total_mark', ''),
                        "exams": exams_info
                    }
                    results.append(result)

            if results:
                return {"success": True, "data": results}
            else:
                return {"error": "Информация о вступительных испытаниях не найдена"}

        except Exception as e:
            return {"error": f"Ошибка при получении данных: {str(e)}"}

    def extract_exam_info_from_api(self, marks_data):
        """
        Извлекает информацию о вступительных испытаниях из API данных
        """
        try:
            exams = []

            for subject, info in marks_data.items():
                mark = info.get('mark', 'Н/Д')
                case = info.get('case', 'Н/Д')
                exams.append(f"{subject}: {mark} ({case})")

            return exams

        except Exception as e:
            print(f"Ошибка при извлечении информации об экзаменах: {e}")
            return []

    def format_result_for_telegram(self, result_data):
        """
        Форматирует результат для отправки в Telegram
        """
        if not result_data.get('success'):
            return f"❌ {result_data.get('error', 'Неизвестная ошибка')}"

        message = "📋 **Информация о вступительных испытаниях:**\n\n"

        for i, application in enumerate(result_data['data'], 1):
            message += f"**{i}. {application['direction']}**\n"
            message += f"📚 Программа: {application['program']}\n"
            message += f"🏛 Институт: {application['institute']}\n"
            message += f"📖 Форма обучения: {application['form']}\n"
            message += f"🎯 Конкурс: {application['competition']}\n"
            message += f"📊 Статус: {application['status']}\n"
            message += f"🔢 Приоритет: {application['priority']}\n"
            message += f"📈 Общий балл: {application['total_mark']}\n"

            message += "\n📝 **Вступительные испытания:**\n"
            for exam in application['exams']:
                message += f"• {exam}\n"

            message += "\n" + "─" * 30 + "\n\n"

        return message


def test_parser():
    """
    Тестирование парсера
    """
    parser = UrfuParser()

    # Тестируем с известным ID
    test_id = "4475115"
    print(f"Тестируем парсер с ID: {test_id}")

    result = parser.search_by_id(test_id)
    print("Результат:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result.get('success'):
        formatted = parser.format_result_for_telegram(result)
        print("\nФорматированный результат для Telegram:")
        print(formatted)


if __name__ == "__main__":
    test_parser()

