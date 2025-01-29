import audio_to_text as aud
from text_analyze import MedicalDataAnalyzer
import os
from datetime import datetime
import shutil
import json

# Директорія для збереження аудіофайлів / Directory for saving audio files
TARGET_DIR = "saved_audio"
os.makedirs(TARGET_DIR, exist_ok=True)

def save_audio(audio_path):
    """Зберігає аудіофайл у цільовій директорії / Saves audio file to target directory"""
    if not audio_path:
        return "Файл не записан!"
    new_filename = "audio.ogg"
    target_path = os.path.join(TARGET_DIR, new_filename)
    shutil.copy2(audio_path, target_path)
    return target_path

def audio_processing_func(audio_input, text_old):
    """Обробляє аудіофайл та додає розпізнаний текст / Processes audio file and appends recognized text"""
    try:
        path_audio = save_audio(audio_input)
        text = aud.audio_analize(path_audio)
        text_old = text_old + ' ' + text
        return text_old
    except Exception as e:
        return f"Помилка обробки аудіо: {str(e)}"

def clear_func():
    """Очищує всі поля в застосунку / Clears all fields in the application"""
    audio_empty = None
    text_empty = ""
    textbox_empty = [""] * 22  # 22 текстових поля
    return [audio_empty, text_empty] + textbox_empty

def text_processing_func(text):
    """Аналізує текст і витягує медичні дані / Analyzes text and extracts medical data"""
    try:
        analyzer = MedicalDataAnalyzer(GOOGLE_API_KEY)
        result = analyzer.analyze_text(text)
        
        # Мапа полів / Field labels mapping
        field_labels = {
            "name": "Ім'я",
            "surname": "Прізвище",
            "patronymic": "По-батькові",
            "gender": "Стать",
            "birth_date": "Дата народження",
            "mobile_phone": "Телефон мобільний",
            "home_phone": "Телефон домашній",
            "residence": "Місце проживання",
            "workplace": "Місце роботи",
            "position": "Посада",
            "dispensary_group": "Диспансерна група",
            "dispensary_group_disease": "Захворювання взяття на диспансерний облік",
            "contingent": "Контингент",
            "certificate_number": "Номер посвідчення",
            "blood_group": "Група крові",
            "rh_factor": "Резус-фактор",
            "blood_transfusions": "Переливання крові",
            "diabetes": "Цукровий діабет",
            "infectious_diseases": "Інфекційні захворювання",
            "surgeries": "Хірургічні втручання",
            "allergy_history": "Алергологічний анамнез",
            "drug_intolerance": "Непереносимість лікарських препаратів"
        }
        
        output_values = [result.get(key, '') for key in field_labels]
        print(output_values)
        return output_values
    except Exception as e:
        return [''] * 22 + [f"Помилка обробки тексту: {str(e)}"]

def download_func(patient_data):
    """Зберігає дані пацієнта у JSON-файл / Saves patient data to a JSON file"""
    try:
        save_dir = "patient_data_json"
        os.makedirs(save_dir, exist_ok=True)
        
        # Генеруємо унікальну назву файлу / Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        patient_name = f"{patient_data.get('surname', '')}_{patient_data.get('name', '')}"
        filename = f"patient_{patient_name}_{timestamp}.json"
        filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))
        filepath = os.path.join(save_dir, filename)
        
        # Записуємо JSON-файл / Save JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(patient_data, f, ensure_ascii=False, indent=4)
        
        print(f"Дані пацієнта збережено у: {filepath}")
        return 0
    except Exception as e:
        print(f"Помилка збереження даних пацієнта: {str(e)}")
        return 1
