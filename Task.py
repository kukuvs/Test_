from datetime import datetime

class Task:
    def __init__(self, id: int, title: str, description: str, category: str, due_date: str, priority: str, status: str = "Не выполнена"):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = self._parse_date(due_date)
        self.priority = priority
        self.status = status

    def _parse_date(self, date_str: str) -> datetime:
        """
        Разбирает строку даты в формате YYYY-MM-DD в объект datetime.

        :param date_str: строка даты
        :return: объект datetime
        :raises ValueError: если строка даты имеет неверный формат
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Неверный формат даты: {date_str}. Используйте формат YYYY-MM-DD.") from e

    def to_dict(self) -> dict:
        """
        Преобразует объект задачи в словарь.

        :return: Словарь, содержащий атрибуты задачи.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "priority": self.priority,
            "status": self.status
        }

    def mark_as_completed(self):
        self.status = "Выполнена"

    def __str__(self):
        """
        Возвращает строковое представление задачи, содержащее ее атрибуты.

        :return: Строковое представление задачи
        """
        return (f"Task ID: {self.id}\n"
                f"Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Category: {self.category}\n"
                f"Due Date: {self.due_date.strftime('%Y-%m-%d')}\n"
                f"Priority: {self.priority}\n"
                f"Status: {self.status}")
