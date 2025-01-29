import audio_to_text as aud
from text_analyze import MedicalDataAnalyzer
import os
from datetime import datetime
import shutil
import json


GOOGLE_API_KEY = "AIzaSyB_83VMQrIQnHNEcY6iDE2SUcSnsGMd1Bw"
# Указываем директорию, куда нужно сохранять файл
TARGET_DIR = "saved_audio"
os.makedirs(TARGET_DIR, exist_ok=True)

def save_audio(audio_path):
    # Проверяем, что файл существует
    if not audio_path:
        return "Файл не записан!"

    # Генерируем уникальное имя файла
    new_filename = f"audio.ogg"
    target_path = os.path.join(TARGET_DIR, new_filename)

    # Копируем файл в целевую директорию
    shutil.copy2(audio_path, target_path)
    return target_path

def audio_processing_func(audio_input,text_old):
    try:
        path_audio = save_audio(audio_input)
        text = aud.audio_analize(path_audio)


        text_old = text_old + ' ' + text


        return text_old
    except Exception as e:
        return f"Помилка обробки аудіо: {str(e)}"


def clear_func():

    # Return empty values for Audio and TextArea
    audio_empty = None
    text_empty = ""

    # Return empty strings for all textboxes (21 fields)
    textbox_empty = [""] * 22

    # Combine all empty values in the correct order
    return [audio_empty, text_empty] + textbox_empty


def text_processing_func(text):
    try:
        analyzer = MedicalDataAnalyzer(GOOGLE_API_KEY)
        result = analyzer.analyze_text(text)

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
        output_values = []
        for key in result:
            output_values.append(result[key])
        print(output_values)
        return output_values
    except Exception as e:
        return [''] * 22 + [f"Помилка обробки тексту: {str(e)}"]


def download_func(patient_data):
    """
    Save patient data as JSON file with timestamp in filename
    """
    try:
        # Create directory if it doesn't exist
        save_dir = "patient_data_json"
        os.makedirs(save_dir, exist_ok=True)

        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create filename with patient name and timestamp
        patient_name = f"{patient_data.get('surname', '')}_{patient_data.get('name', '')}"
        filename = f"patient_{patient_name}_{timestamp}.json"

        # Clean filename of any invalid characters
        filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))

        # Full path for saving
        filepath = os.path.join(save_dir, filename)

        # Save data as JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(patient_data, f, ensure_ascii=False, indent=4)

        print(f"Patient data saved to: {filepath}")
        return 0

    except Exception as e:
        print(f"Error saving patient data: {str(e)}")
        return 1

def clear_func():
    """Clear all fields in the application"""
    # Return empty values for Audio and TextArea
    audio_empty = None
    text_empty = ""

    # Return empty strings for all textboxes (21 fields)
    textbox_empty = [""] * 22

    # Combine all empty values in the correct order
    return [audio_empty, text_empty] + textbox_empty