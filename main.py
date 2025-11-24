import json
import os
from datetime import date


DATA_FILE = os.path.join(os.getcwd(), "mood.json")
DATE_FMT = "%Y-%m-%d"

MOODS = {
    1: "Очень плохо",
    2: "Плохо",
    3: "Нормально",
    4: "Хорошо",
    5: "Отлично"
}

# ------------------------------------------------------
# Модель одной записи настроения
# ------------------------------------------------------
class MoodEntry:
    def __init__(self, mood, note=""):
        self.mood = mood
        self.note = note.strip()

    def to_dict(self):
        return {
            "mood": self.mood,
            "note": self.note
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["mood"], d.get("note", ""))


# ------------------------------------------------------
# Репозиторий — чтение/запись mood.json
# ------------------------------------------------------
class MoodRepository:
    def __init__(self, file_path=DATA_FILE):
        self.file_path = file_path

    def load(self):
        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                data = {}
                for d, info in raw.items():
                    data[d] = MoodEntry.from_dict(info)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save(self, data: dict):
        raw = {d: entry.to_dict() for d, entry in data.items()}

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=4)


# ------------------------------------------------------
# Логика приложения
# ------------------------------------------------------
class MoodTracker:
    def __init__(self, repo: MoodRepository):
        self.repo = repo

    def add_mood(self):
        today = date.today().strftime(DATE_FMT)
        data = self.repo.load()

        print("Выбери настроение:")
        for key, value in MOODS.items():
            print(f"{key}. {value}")

        while True:
            try:
                key = int(input("Введите номер: "))
                if key in MOODS:
                    break
            except ValueError:
                pass
            print("Некорректный выбор!")

        note = input("Заметка (можно пусто): ").strip()
        entry = MoodEntry(MOODS[key], note)

        data[today] = entry
        self.repo.save(data)

        print("Настроение сохранено.")

    def view_day(self):
        d = input("Введите дату (YYYY-MM-DD). Пусто = сегодня: ").strip()
        if not d:
            d = date.today().strftime(DATE_FMT)

        data = self.repo.load()

        if d not in data:
            print("Нет данных за эту дату.")
            return

        entry = data[d]
        print(f"Дата: {d}")
        print(f"Настроение: {entry.mood}")
        print(f"Заметка: {entry.note}")

    def show_all(self):
        data = self.repo.load()

        if not data:
            print("Записей пока нет.")
            return

        for d, entry in sorted(data.items()):
            print(f"{d}: {entry.mood} — {entry.note}")

    def delete_mood(self):
        d = input("Введите дату для удаления (YYYY-MM-DD). Пусто = сегодня: ").strip()
        if not d:
            d = date.today().strftime(DATE_FMT)

        data = self.repo.load()

        if d not in data:
            print("Нет записи за эту дату.")
            return

        entry = data[d]
        print(f"Запись найдена: {entry.mood} — {entry.note}")

        confirm = input("Удалить? (y/n): ").strip().lower()
        if confirm == "y":
            del data[d]
            self.repo.save(data)
            print("Запись удалена.")
        else:
            print("Удаление отменено.")


# ------------------------------------------------------
# Пример запуска
# ------------------------------------------------------
if __name__ == "__main__":
    repo = MoodRepository()
    tracker = MoodTracker(repo)

    while True:
        print("\n1. Добавить настроение")
        print("2. Посмотреть за день")
        print("3. Показать все записи")
        print("4. Удалить запись")
        print("5. Выход")

        choice = input("Выбор: ").strip()
        if choice == "1":
            tracker.add_mood()
        elif choice == "2":
            tracker.view_day()
        elif choice == "3":
            tracker.show_all()
        elif choice == "4":
            tracker.delete_mood()
        elif choice == "5":
            break
        else:
            print("Некорректный ввод.")
