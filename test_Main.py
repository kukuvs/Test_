import pytest
from unittest.mock import patch, MagicMock
from TaskManager import TaskManager
from Main import handle_add_task, handle_delete_task, handle_edit_task, handle_view_tasks, handle_search_tasks, handle_mark_completed


@pytest.fixture
def mock_manager():
    """Создает мок для TaskManager."""
    manager = MagicMock(spec=TaskManager)
    manager.view_tasks.return_value = []
    manager.search_tasks.return_value = []
    manager.find_task_by_id.return_value = None
    return manager


def test_handle_add_task(mock_manager):
    """Тестирует добавление задачи."""
    inputs = ["Задача 1", "Описание", "Работа", "2024-12-01", "высокий"]
    with patch("builtins.input", side_effect=inputs):
        handle_add_task(mock_manager)
    mock_manager.add_task.assert_called_once_with("Задача 1", "Описание", "Работа", "2024-12-01", "высокий")


def test_handle_delete_task(mock_manager):
    """Тестирует удаление задачи."""
    with patch("builtins.input", side_effect=["1"]):
        handle_delete_task(mock_manager)
    mock_manager.delete_task.assert_called_once_with(1)


def test_handle_delete_task_invalid_id(mock_manager, capsys):
    """Тестирует удаление задачи с некорректным ID."""
    with patch("builtins.input", side_effect=["abc"]):
        handle_delete_task(mock_manager)
    captured = capsys.readouterr()
    assert "Неверный формат ID." in captured.out
    mock_manager.delete_task.assert_not_called()


def test_handle_edit_task(mock_manager):
    """Тестирует редактирование задачи."""
    inputs = ["1", "y", "Новый заголовок", "y", "Новое описание", "n", "n", "n"]
    with patch("builtins.input", side_effect=inputs):
        handle_edit_task(mock_manager)
    mock_manager.edit_task.assert_called_once_with(1, title="Новый заголовок", description="Новое описание")


def test_handle_edit_task_invalid_id(mock_manager, capsys):
    """Тестирует редактирование задачи с некорректным ID."""
    with patch("builtins.input", side_effect=["abc"]):
        handle_edit_task(mock_manager)
    captured = capsys.readouterr()
    assert "Неверный формат ID." in captured.out
    mock_manager.edit_task.assert_not_called()


def test_handle_view_tasks_no_tasks(mock_manager, capsys):
    """Тестирует просмотр задач при отсутствии задач."""
    mock_manager.view_tasks.return_value = []
    with patch("builtins.input", side_effect=[""]):
        handle_view_tasks(mock_manager)
    captured = capsys.readouterr()
    assert "Задач не найдено." in captured.out


def test_handle_search_tasks_no_results(mock_manager, capsys):
    """Тестирует поиск задач без результатов."""
    mock_manager.search_tasks.return_value = []
    inputs = ["ключевое слово", "Работа", "выполнено"]
    with patch("builtins.input", side_effect=inputs):
        handle_search_tasks(mock_manager)
    captured = capsys.readouterr()
    assert "Задач не найдено." in captured.out


def test_handle_mark_completed(mock_manager):
    """Тестирует отметку задачи как выполненной."""
    mock_manager.find_task_by_id.return_value = MagicMock()
    with patch("builtins.input", side_effect=["1"]):
        handle_mark_completed(mock_manager)
    mock_manager.edit_task.assert_called_once_with(1, status="выполнено")


def test_handle_mark_completed_task_not_found(mock_manager, capsys):
    """Тестирует отметку задачи как выполненной, если задача не найдена."""
    mock_manager.find_task_by_id.return_value = None
    with patch("builtins.input", side_effect=["1"]):
        handle_mark_completed(mock_manager)
    captured = capsys.readouterr()
    assert "Задача не найдена." in captured.out
    mock_manager.edit_task.assert_not_called()
