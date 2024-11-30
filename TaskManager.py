import json
import os
from typing import List, Optional, Dict, Any
from Task import Task


class TaskManager:
    def __init__(self, file_path: str) -> None:
        """
        Инициализирует TaskManager, создавая файл задач, если он не существует.
        :param file_path: путь к файлу задач.
        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Создает файл задач, если он не существует.
        """
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)

    def load_tasks(self) -> List[Task]:
        """
        Загружает все задачи из файла.
        :return: список задач.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Сохраняет задачи в файл с красивым форматированием.
        :param tasks: список задач.
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in tasks], file, indent=4, ensure_ascii=False)

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Ищет задачу по ID, не загружая все данные.
        :param task_id: ID задачи.
        :return: Найденная задача или None.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return next((Task(**task) for task in json.load(file) if task["id"] == task_id), None)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def add_task(self, title: str, description: str, category: str, due_date: str, priority: str) -> None:
        """
        Добавляет новую задачу в список.
        :param title: заголовок задачи.
        :param description: описание задачи.
        :param category: категория задачи.
        :param due_date: дата выполнения задачи.
        :param priority: приоритет задачи.
        """
        if not all([title, description, category, due_date, priority]):
            print("Ошибка: все поля задачи должны быть заполнены.")
            return

        tasks = self.load_tasks()

        if any(task.title == title for task in tasks):
            print("Ошибка: задача с таким заголовком уже существует.")
            return

        # Генерация ID для новой задачи
        new_id = (max(task.id for task in tasks) + 1) if tasks else 1
        new_task = Task(id=new_id, title=title, description=description, category=category, due_date=due_date, priority=priority)
        tasks.append(new_task)
        self.save_tasks(tasks)

    def delete_task(self, task_id: int) -> None:
        """
        Удаляет задачу по ID с минимальной загрузкой данных.
        :param task_id: ID задачи.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                tasks = json.load(file)

            updated_tasks = [task for task in tasks if task["id"] != task_id]  # Исключение задачи с указанным ID
            if len(updated_tasks) == len(tasks):
                print(f"Задача с ID {task_id} не найдена.")
                return

            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(updated_tasks, file, indent=4, ensure_ascii=False)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Ошибка при удалении задачи.")

    def edit_task(self, task_id: int, **kwargs: Dict[str, Any]) -> None:
        """
        Редактирует задачу по ее ID, минимизируя загрузку данных.
        :param task_id: ID задачи.
        :param kwargs: новые значения полей задачи.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                tasks = json.load(file)

            updated_tasks = []
            found = False
            for task_data in tasks:
                if task_data["id"] == task_id:
                    task = Task(**task_data)
                    found = True
                    # Применение изменений к задаче
                    for key, value in kwargs.items():
                        if hasattr(task, key):
                            setattr(task, key, value)
                    updated_tasks.append(task.to_dict())
                else:
                    updated_tasks.append(task_data)

            if not found:
                print(f"Задача с ID {task_id} не найдена.")
                return

            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(updated_tasks, file, indent=4, ensure_ascii=False)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Ошибка при редактировании задачи.")

    def search_tasks(self, keyword: Optional[str] = None,
                    category: Optional[str] = None,
                    status: Optional[str] = None) -> List[Task]:
        """
        Ищет задачи по критериям.
        :param keyword: ключевое слово для поиска.
        :param category: категория для поиска.
        :param status: статус для поиска.
        :return: список найденных задач.
        """
        result = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for task_data in json.load(file):
                    # Фильтрация задач по критериям
                    if (
                        (not keyword or keyword.lower() in task_data["title"].lower() or keyword.lower() in task_data["description"].lower())
                        and (not category or task_data["category"] == category)
                        and (not status or task_data["status"] == status)
                    ):
                        result.append(Task(**task_data))
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return result

    def view_tasks(self, category: Optional[str] = None) -> List[Task]:
        """
        Показывает список задач.
        :param category: категория для фильтрации.
        :return: список задач.
        """
        tasks = self.load_tasks()
        return [task for task in tasks if task.category == category] if category else tasks

    def mark_task_as_completed(self, task_id: int):
        """
        Отмечает задачу как выполненную.
        :param task_id: ID задачи.
        :raises ValueError: если задача не найдена.
        """
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:  # Сравниваем по ID задачи
                task.status = 'Выполнена'  # Исправляем статус на правильный
                self.save_tasks(tasks)  # Сохраняем задачи обратно в файл
                return
        raise ValueError("Задача не найдена")

