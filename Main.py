from TaskManager import TaskManager

def main():
    manager = TaskManager("tasks.json")
    while True:
        print("\nМенеджер задач")
        print("1. Просмотреть все задачи")
        print("2. Добавить задачу")
        print("3. Редактировать задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")
        print("6. Отметить задачу как выполненную")
        print("7. Выйти")

        choice = input("Выберите действие: ")
        if choice == "1":
            tasks = manager.view_tasks()
            for task in tasks:
                print("\n",task)
        elif choice == "2":
            title = input("Название: ")
            description = input("Описание: ")
            category = input("Категория: ")
            due_date = input("Срок выполнения (YYYY-MM-DD): ")
            priority = input("Приоритет (Низкий/Средний/Высокий): ")
            manager.add_task(title, description, category, due_date, priority)
            
        elif choice == "3":
            task_id = int(input("ID задачи для редактирования: "))
            title = input("Новое название (оставьте пустым для пропуска): ")
            description = input("Новое описание (оставьте пустым для пропуска): ")
            category = input("Новая категория (оставьте пустым для пропуска): ")
            due_date = input("Новый срок выполнения (YYYY-MM-DD, оставьте пустым для пропуска): ")
            priority = input("Новый приоритет (оставьте пустым для пропуска): ")
            updates = {k: v for k, v in locals().items() if v and k != "task_id"}
            manager.edit_task(task_id, **updates)
            
        elif choice == "4":
            task_id = int(input("ID задачи для удаления: "))
            manager.delete_task(task_id)
            
        elif choice == "5":
            keyword = input("Ключевое слово: ")
            category = input("Категория: ")
            status = input("Статус (Выполнена/Не выполнена): ")
            results = manager.search_tasks(keyword=keyword, category=category, status=status)
            for task in results:
                print(task)
                
        elif choice == "6":
            task_id = int(input("ID задачи для отметки как выполненной: "))
            manager.mark_task_as_completed(task_id)
            
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
