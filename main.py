import json
from datetime import datetime
import os
import sys
import locale

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
locale.setlocale(locale.LC_ALL, '')

def add_note():
    title = input("Введите заголовок заметки: ")
    body = input("Введите тело заметки: ")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    note = {
        "id": len(notes) + 1,
        "title": title,
        "body": body,
        "created_at": current_time,
        "last_updated": current_time
    }

    notes.append(note)
    save_notes()
    print("Заметка успешно сохранена")

    notes.append(note)
    save_notes()
    print("Заметка успешно сохранена")

def save_notes():
    with open('notes.json', 'w') as file:
        json.dump(notes, file, indent=4)

def read_notes():
    if not os.path.exists('notes.json'):
        with open('notes.json', 'w') as file:
            json.dump([], file)
            return []

    with open('notes.json', 'r') as file:
        try:
            loaded_notes = json.load(file)
            for note in loaded_notes:
                if 'created_at' not in note:
                    note['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if 'last_updated' not in note:
                    note['last_updated'] = note['created_at']
            return loaded_notes
        except json.decoder.JSONDecodeError:
            return []


def list_notes():
    filter_date = input("Введите дату для фильтрации (гггг-мм-дд): ")
    filtered_notes = [note for note in notes if note['created_at'].startswith(filter_date) or note['last_updated'].startswith(filter_date)]
    
    if filtered_notes:
        print("Список заметок:")
        for note in filtered_notes:
            print(f"ID: {note['id']}, Заголовок: {note['title']}, Время создания: {note['created_at']}, Время последнего обновления: {note['last_updated']}")
    else:
        print("Нет заметок на указанную дату")

def read_note_by_id():
    note_id = int(input("Введите ID заметки для чтения: "))
    for note in notes:
        if note['id'] == note_id:
            print(f"Заголовок: {note['title']}")
            print(f"Тело заметки: {note['body']}")
            print(f"Дата создания: {note['created_at']}")
            print(f"Дата последнего обновления: {note['last_updated']}")
            return
    print("Заметка с указанным ID не найдена")

def edit_note_by_id():
    note_id = int(input("Введите ID заметки для редактирования: "))
    for note in notes:
        if note['id'] == note_id:
            new_title = input("Введите новый заголовок (оставьте пустым для сохранения текущего): ")
            new_body = input("Введите новое тело заметки (оставьте пустым для сохранения текущего): ")

            if new_title:
                note['title'] = new_title
            if new_body:
                note['body'] = new_body

            note['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_notes()
            print("Заметка успешно отредактирована")
            return
    print("Заметка с указанным ID не найдена")

def delete_note_by_id():
    note_id = int(input("Введите ID заметки для удаления: "))
    for note in notes:
        if note['id'] == note_id:
            notes.remove(note)
            save_notes()
            print("Заметка успешно удалена")
            return
    print("Заметка с указанным ID не найдена")

notes = read_notes()

while True:
    command = input("Введите команду (add, read, edit, delete, list, exit): ")

    if command == "add":
        add_note()
    elif command == "read":
        read_note_by_id()
    elif command == "edit":
        edit_note_by_id()
    elif command == "delete":
        delete_note_by_id()
    elif command == "list":
        list_notes()
    elif command == "exit":
        break
    else:
        print("Некорректная команда")
