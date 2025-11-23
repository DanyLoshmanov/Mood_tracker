import json
import os
from datetime import date ,datetime, timedelta as dt

DATA_FILE = os.path.join(os.getcwd(), 'mood.json')
DATA_FMT = '%Y-%m-%d'

MOODS = {
    1: 'Очень плохо',
    2: 'Плохо',
    3: 'Нормально',
    4: 'Хорошо',
    5: 'Отлично'
}

def load_data():
    if not os.path.exists(DATA_FILE):
        print("Невозможно найти файл!")
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_mood():
    today = date.today().strftime(DATA_FMT)
    data = load_data()

    print("Введите цифру вашего настроения: ")
    for key, value in MOODS.items():
        print(f"{key}. {value}")