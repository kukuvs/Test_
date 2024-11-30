import sys
from TaskManager import TaskManager


def display_menu() -> None:
    """Выводит меню программы."""
    menu_options = [
        "1. Добавить задачу",
        "2. Удалить задачу",
        "3. Редактировать задачу",
        "4. Просмотреть задачи",
        "5. Найти задачу",
        "6. Отметить задачу как выполненную",
        "7. Выход",
    ]
    print("\nTask Manager")
    print("\n".join(menu_options))


def get_task_updates() -> dict:
    """Запрашивает у пользователя обновления для задачи."""
    updates = {}
    fields = {
        "title": "Новый заголовок",
        "description": "Новое описание",
        "category": "Новая категория",
        "due_date": "Новая дата выполнения (YYYY-MM-DD)",
        "priority": "Новый приоритет (низкий/средний/высокий)",
    }

    for field, prompt in fields.items():
        if input(f"Изменить {field}? (y/n): ").lower() == "y":
            updates[field] = input(f"{prompt}: ")

    return updates


def handle_add_task(manager: TaskManager) -> None:
    """Обрабатывает добавление новой задачи."""
    title = input("Введите заголовок: ")
    description = input("Введите описание: ")
    category = input("Введите категорию: ")
    due_date = input("Введите дату выполнения (YYYY-MM-DD): ")
    priority = input("Введите приоритет (низкий/средний/высокий): ")

    manager.add_task(title, description, category, due_date, priority)
    print("Задача добавлена.")


def handle_delete_task(manager: TaskManager) -> None:
    """Обрабатывает удаление задачи."""
    try:
        task_id = int(input("Введите ID задачи для удаления: "))
        manager.delete_task(task_id)
        print("Задача удалена.")
    except ValueError:
        print("Неверный формат ID.")


def handle_edit_task(manager: TaskManager) -> None:
    """Обрабатывает редактирование задачи."""
    try:
        task_id = int(input("Введите ID задачи для редактирования: "))
        updates = get_task_updates()
        manager.edit_task(task_id, **updates)
        print("Задача отредактирована.")
    except ValueError:
        print("Неверный формат ID.")


def handle_view_tasks(manager: TaskManager) -> None:
    """Обрабатывает просмотр задач."""
    category = input("Введите категорию (нажмите Enter для всех категорий): ")
    tasks = manager.view_tasks(category if category else None)

    if tasks:
        for task in tasks:
            print(f"\n {task}")
    else:
        print("Задач не найдено.")


def handle_search_tasks(manager: TaskManager) -> None:
    """Обрабатывает поиск задач."""
    keyword = input("Введите ключевое слово для поиска: ")
    category = input("Введите категорию (нажмите Enter для всех категорий): ")
    status = input("Введите статус (выполнено/не выполнено/нажмите Enter для всех): ")

    tasks = manager.search_tasks(keyword, category if category else None, status if status else None)
    if tasks:
        for task in tasks:
            print(task)
    else:
        print("Задач не найдено.")


def handle_mark_completed(manager: TaskManager) -> None:
    """Обрабатывает отметку задачи как выполненной."""
    try:
        task_id = int(input("Введите ID задачи для отметки как выполненной: "))
        task = manager.find_task_by_id(task_id)
        if task:
            manager.edit_task(task_id, status="выполнено")
            print("Задача отмечена как выполненная.")
        else:
            print("Задача не найдена.")
    except ValueError:
        print("Неверный формат ID.")


def main():
    file_path = "tasks.json"  # Укажите путь к файлу с задачами
    manager = TaskManager(file_path)

    actions = {
        "1": handle_add_task,
        "2": handle_delete_task,
        "3": handle_edit_task,
        "4": handle_view_tasks,
        "5": handle_search_tasks,
        "6": handle_mark_completed,
        "7": lambda _: sys.exit(0),
    }

    while True:
        display_menu()
        choice = input("Выберите действие: ")

        action = actions.get(choice)
        if action:
            action(manager)
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
