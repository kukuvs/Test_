import pytest
from Task import Task

def test_task_creation():
    task = Task(1, "Test Task", "Description", "Work", "2024-12-01", "High")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Description"
    assert task.category == "Work"
    assert task.due_date.strftime("%Y-%m-%d") == "2024-12-01"
    assert task.priority == "High"
    assert task.status == "Не выполнена"

def test_task_to_dict():
    task = Task(1, "Test Task", "Description", "Work", "2024-12-01", "High")
    task_dict = task.to_dict()
    assert task_dict == {
        "id": 1,
        "title": "Test Task",
        "description": "Description",
        "category": "Work",
        "due_date": "2024-12-01",
        "priority": "High",
        "status": "Не выполнена"
    }

def test_mark_as_completed():
    task = Task(1, "Test Task", "Description", "Work", "2024-12-01", "High")
    task.mark_as_completed()
    assert task.status == "Выполнена"

def test_task_str():
    task = Task(1, "Test Task", "Description", "Work", "2024-12-01", "High")
    task_str = str(task)
    expected_str = (
        "Task ID: 1\n"
        "Title: Test Task\n"
        "Description: Description\n"
        "Category: Work\n"
        "Due Date: 2024-12-01\n"
        "Priority: High\n"
        "Status: Не выполнена"
    )
    assert task_str == expected_str

def test_invalid_date_format():
    with pytest.raises(ValueError, match="Неверный формат даты: invalid-date. Используйте формат YYYY-MM-DD."):
        Task(1, "Invalid Date Task", "Description", "Work", "invalid-date", "High")

def test_task_equality():
    task1 = Task(1, "Task 1", "Description 1", "Work", "2024-12-01", "High")
    task2 = Task(1, "Task 1", "Description 1", "Work", "2024-12-01", "High")
    assert task1.to_dict() == task2.to_dict()

def test_task_priority():
    task = Task(1, "Test Task", "Description", "Work", "2024-12-01", "Low")
    assert task.priority == "Low"
    task.priority = "High"
    assert task.priority == "High"

def test_task_missing_fields():
    with pytest.raises(TypeError):
        Task(1, "Test Task", "Description", "Work", "2024-12-01")  # Отсутствует `priority`
