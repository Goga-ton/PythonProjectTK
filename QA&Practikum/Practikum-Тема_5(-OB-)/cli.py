import sys
from note import Note
import db

def print_notes(notes):
    if not notes:
        print("Заметок нет")
        return
    for note in notes:
        print(f"ID: {note.id}\nЗаголовок: {note.title}\nТекст: {note.content}\nСоздано: {note.created_at}")

def main():
    db.init_db()
    while True:
        print("\nВыберите действие:")
        print("\n1. Показать все заметки:")
        print("2. Добавить заметку:")
        print("3. Удалить заметку:")
        print("4. Редактировать заметку:")
        print("5. Выйти:")
        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            notes = db.get_notes()
            print_notes(notes)

        elif choice == "2":
            title = input("Заголовок: ").strip()
            content = input("Текст: ").strip()
            note = Note(title, content)
            db.add_note(note)
            print("Заметка добавлена!")

        elif choice == "3":
            note_id = input("ID заметки для удаления: ").strip()
            if note_id.isdigit():
                db.delete_note(int(note_id))
                print("Заметка удалена!")
            else:
                print("Некорректный ID!")

        elif choice == "4":
            note_id = input("ID заметки для редактирования: ").strip()
            if note_id.isdigit():
                note_id = int(note_id)
                notes = db.get_notes()
                note_exists = any(note.id == note_id for note in notes)

                if note_exists:
                    new_title = input("Новый заголовок: ").strip()
                    new_content = input("Новый текст: ").strip()

                    if new_title or new_content:
                        db.update_note(note_id, new_title, new_content)
                        print("Заметка обновлена!")
                    else:
                        print("Не введены новые данные!")
                else:
                    print("Заметка с таким ID не найдена!")
            else:
                print("Некорректный ID!")

        elif choice == "5":
            print("До свидания!")
            sys.exit()

        else:
            print("Некорректный выбор! Попробуйте снова.")

