import os

from Main import main
from TaskManager import TaskManager

def test_main_view_tasks(tmpdir, capsys):
    """
    Тестирование просмотра всех задач
    """
    file_path = os.path.join(tmpdir, 'tasks.json')
    manager = TaskManager(file_path)
    manager.add_task('Task 1', 'Description 1', 'Work', '2024-12-01', 'High')
    manager.add_task('Task 2', 'Description 2', 'Personal', '2024-12-02', 'Low')

    main()

    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out

def test_main_add_task(tmpdir, capsys):
    """
    Тестирование добавления задачи
    """
    file_path = os.path.join(tmpdir, 'tasks.json')
    manager = TaskManager(file_path)

    main()

    captured = capsys.readouterr()
    assert "Название: " in captured.out
    assert "Описание: " in captured.out
    assert "Категория: " in captured.out
    assert "Срок выполнения (YYYY-MM-DD): " in captured.out
    assert "Приоритет (Низкий/Средний/Высокий): " in captured.out

def test_main_edit_task(tmpdir, capsys):
    """
    Тестирование редактирования задачи
    """
    file_path = os.path.join(tmpdir, 'tasks.json')
    manager = TaskManager(file_path)
    manager.add_task('Task 1', 'Description 1', 'Work', '2024-12-01', 'High')

    main()

    captured = capsys.readouterr()
    assert "ID задачи для редактирования: " in captured.out
    assert "Новое название (оставьте пустым для пропуска): " in captured.out
    assert "Новое описание (оставьте пустым для пропуска): " in captured.out
    assert "Новая категория (оставьте пустым для пропуска): " in captured.out
    assert "Новый срок выполнения (YYYY-MM-DD, оставьте пустым для пропуска): " in captured.out
    assert "Новый приоритет (оставьте пустым для пропуска): " in captured.out

def test_main_delete_task(tmpdir, capsys):
    """
    Тестирование удаления задачи
    """
    file_path = os.path.join(tmpdir, 'tasks.json')
    manager = TaskManager(file_path)
    manager.add_task('Task 1', 'Description 1', 'Work', '2024-12-01', 'High')

    main()

    captured = capsys.readouterr()
    assert "ID задачи для удаления: " in captured.out

def test_main_search_tasks(tmpdir, capsys):
    """
    Тестирование поиска задач
    """
    file_path = os.path.join(tmpdir, 'tasks.json')
    manager = TaskManager(file_path)
    manager.add_task('Task 1', 'Description 1', 'Work', '2024-12-01', 'High')
    manager.add_task('Task 2', 'Description 2', 'Personal', '2024-12-02', 'Low')

    main()

    captured = capsys.readouterr()
    assert "Ключевое слово: " in captured.out
    assert "Категория: " in captured.out
    assert "Статус (Выполнена/Не выполнена): " in captured.out

def test_main_mark_task_as_completed(tmpdir, capsys):
    """
    Тестирование отметки задачи как выполненной
    """
    file_path = os.path.join(tmpdir, 'tasks.json')
    manager = TaskManager(file_path)
    manager.add_task('Task 1', 'Description 1', 'Work', '2024-12-01', 'High')

    main()

    captured = capsys.readouterr()
    assert "ID задачи для отметки как выполненной: " in captured.out
