import os 
import json
from TaskManager import TaskManager
from Task import Task

def test_task_manager_init(tmpdir):
    file_path = os.path.join(tmpdir, 'tasks.json')
    task_manager = TaskManager(file_path)
    assert os.path.exists(file_path)

def test_task_manager_load_tasks(tmpdir):
    file_path = os.path.join(tmpdir, 'tasks.json')
    task_manager = TaskManager(file_path)
    assert task_manager.load_tasks() == []

    with open(file_path, 'w') as file:
        json.dump([
            {'id': 1, 'title': 'Task 1', 'description': 'Description 1', 'category': 'Work', 'due_date': '2024-12-01', 'priority': 'High'},
            {'id': 2, 'title': 'Task 2', 'description': 'Description 2', 'category': 'Personal', 'due_date': '2024-12-02', 'priority': 'Medium'},
        ], file)

    tasks = task_manager.load_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == 'Task 1'
    assert tasks[1].category == 'Personal'

def test_task_manager_save_tasks(tmpdir):
    file_path = os.path.join(tmpdir, 'tasks.json')
    task_manager = TaskManager(file_path)
    tasks = [
        Task(1, 'Task 1', 'Description 1', 'Work', '2024-12-01', 'High'),
        Task(2, 'Task 2', 'Description 2', 'Personal', '2024-12-02', 'Medium'),
    ]
    task_manager.save_tasks(tasks)

    with open(file_path, 'r') as file:
        saved_tasks = json.load(file)
    assert len(saved_tasks) == 2
    assert saved_tasks[0]['title'] == 'Task 1'
    assert saved_tasks[1]['category'] == 'Personal'

def test_task_manager_add_task(tmpdir):
    file_path = os.path.join(tmpdir, 'tasks.json')
    task_manager = TaskManager(file_path)
    task_manager.add_task('Task 3', 'Description 3', 'Work', '2024-12-03', 'Low')

    tasks = task_manager.load_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == 'Task 3'

def test_task_manager_delete_task(tmpdir):
    file_path = os.path.join(tmpdir, 'tasks.json')
    task_manager = TaskManager(file_path)
    task_manager.add_task('Task 3', 'Description 3', 'Work', '2024-12-03', 'Low')
    task_manager.delete_task(1)

    tasks = task_manager.load_tasks()
    assert len(tasks) == 0

def test_task_manager_edit_task(tmpdir):
    file_path = os.path.join(tmpdir, 'tasks.json')
    task_manager = TaskManager(file_path)
    task_manager.add_task('Task 3', 'Description 3', 'Work', '2024-12-03', 'Low')
    task_manager.edit_task(1, title='Edited Task 3', category='Personal')

    tasks = task_manager.load_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == 'Edited Task 3'
    assert tasks[0].category == 'Personal'

def test_task_manager_mark_task_as_completed(tmpdir):
    file_path = os.path.join(tmpdir, 'tasks.json')
    task_manager = TaskManager(file_path)
    task_manager.add_task('Task 3', 'Description 3', 'Work', '2024-12-03', 'Low')
    task_manager.mark_task_as_completed(1)

    tasks = task_manager.load_tasks()
    assert len(tasks) == 1
    assert tasks[0].status == 'Выполнена'

def test_task_manager_search_tasks(tmpdir):
    file_path = os.path.join(tmpdir, 'tasks.json')
    task_manager = TaskManager(file_path)
    task_manager.add_task('Task 3', 'Description 3', 'Work', '2024-12-03', 'Low')
    task_manager.add_task('Task 4', 'Description 4', 'Personal', '2024-12-04', 'High')

    tasks = task_manager.search_tasks(keyword='Task 3')
    assert len(tasks) == 1
    assert tasks[0].title == 'Task 3'

    tasks = task_manager.search_tasks(category='Personal')
    assert len(tasks) == 1
    assert tasks[0].category == 'Personal'

    tasks = task_manager.search_tasks(status='Выполнена')
    assert len(tasks) == 0

def test_task_manager_view_tasks(tmpdir):
    file_path = os.path.join(tmpdir, 'tasks.json')
    task_manager = TaskManager(file_path)
    task_manager.add_task('Task 3', 'Description 3', 'Work', '2024-12-03', 'Low')
    task_manager.add_task('Task 4', 'Description 4', 'Personal', '2024-12-04', 'High')

    tasks = task_manager.view_tasks(category='Work')
    assert len(tasks) == 1
    assert tasks[0].category == 'Work'

    tasks = task_manager.view_tasks()
    assert len(tasks) == 2
