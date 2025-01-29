import gradio as gr
import app_function as func
import document_import as doci
import uvicorn

# Словник для підписів полів (назви полів у формі) / Dictionary for field labels
field_labels = {
    "name": "Ім'я",  # Name
    "surname": "Прізвище",  # Surname
    "patronymic": "По-батькові",  # Patronymic
    "gender": "Стать",  # Gender
    "birth_date": "Дата народження",  # Birth Date
    "mobile_phone": "Телефон мобільний",  # Mobile Phone
    "home_phone": "Телефон домашній",  # Home Phone
    "residence": "Місце проживання",  # Residence
    "workplace": "Місце роботи",  # Workplace
    "position": "Посада",  # Position
    "dispensary_group": "Диспансерна група",  # Dispensary Group
    "dispensary_group_disease": "Захворювання взяття на диспансерний облік",  # Disease under Dispensary Registration
    "contingent": "Контингент",  # Contingent
    "certificate_number": "Номер посвідчення",  # Certificate Number
    "blood_group": "Група крові",  # Blood Group
    "rh_factor": "Резус-фактор",  # Rh Factor
    "blood_transfusions": "Переливання крові",  # Blood Transfusions
    "diabetes": "Цукровий діабет",  # Diabetes
    "infectious_diseases": "Інфекційні захворювання",  # Infectious Diseases
    "surgeries": "Хірургічні втручання",  # Surgeries
    "allergy_history": "Алергологічний анамнез",  # Allergy History
    "drug_intolerance": "Непереносимість лікарських препаратів"  # Drug Intolerance
}

# Ініціалізація словника patient_data пустими значеннями / Initialize patient_data dictionary with empty values
patient_data = {key: '' for key in field_labels.keys()}

# Функція збору даних пацієнта / Function to collect patient data
def collect_patient_data(*values):
    current_data = {}
    doci.docx_info_add(patient_data)  # Додає інформацію в документ / Adds information to document
    for key, value in zip(field_labels.keys(), values):
        current_data[key] = value
    return func.download_func(current_data)  # Викликає функцію завантаження / Calls the download function

# Функція оновлення даних пацієнта / Function to update patient data
def update_patient_data(key, value):
    patient_data[key] = value  # Оновлює значення у словнику / Updates value in dictionary
    return value

# Функція відображення даних пацієнта / Function to display patient data
def display_patient_data():
    output = "\n".join([f"{field_labels[key]}: {value}" for key, value in patient_data.items() if value])
    print(output)
    print(patient_data)
    print(text)
    # Повертає список значень для всіх текстових полів / Returns a list of values for all textboxes
    return [patient_data.get(key, '') for key in field_labels.keys()] + ["Немає даних" if not output else output]

# Інтерфейс Gradio / Gradio Interface
with gr.Blocks(css=".large-textbox { font-size: 20px; }") as demo:
    gr.Markdown("# Автоматизація медичних даних")  # Header / Заголовок

    with gr.Row():
        with gr.Column():
            # Ввід аудіо / Audio input
            audio_input = gr.Audio(type="filepath", label="Записуйте свій голос")
            audio_processing_button = gr.Button("Обробка аудіо")  # Process audio button
            text = gr.TextArea(label="Текст", lines=8, interactive=True)

            text_processing_button = gr.Button("Аналіз тексту")  # Analyze text button

            with gr.Row():
                download_button = gr.Button("Завантажити дані")  # Download button
                clear_button = gr.Button("Очистити дані")  # Clear button

        with gr.Column():
            textboxes = {}  # Словник для збереження текстових полів / Dictionary for storing textboxes
            with gr.Row():
                with gr.Column():
                    # Перша половина текстових полів / First half of textboxes
                    for key in list(field_labels.keys())[:12]:
                        textboxes[key] = gr.Textbox(
                            value=patient_data[key],
                            label=field_labels[key],
                            lines=1,
                            interactive=True
                        )
                        textboxes[key].change(
                            update_patient_data,
                            inputs=[gr.Textbox(value=key, visible=False), textboxes[key]],
                            outputs=textboxes[key]
                        )
                with gr.Column():
                    # Друга половина текстових полів / Second half of textboxes
                    for key in list(field_labels.keys())[12:]:
                        textboxes[key] = gr.Textbox(
                            value=patient_data[key],
                            label=field_labels[key],
                            lines=1,
                            interactive=True
                        )
                        textboxes[key].change(
                            update_patient_data,
                            inputs=[gr.Textbox(value=key, visible=False), textboxes[key]],
                            outputs=textboxes[key]
                        )
            # Зв’язок віджетів із функціями / Connect widgets to functions
            audio_processing_button.click(func.audio_processing_func, inputs=[audio_input, text], outputs=text)
            clear_button.click(
                func.clear_func,
                inputs=None,
                outputs=[audio_input, text] + [textboxes[key] for key in field_labels.keys()]
            )
            text_processing_button.click(
                func.text_processing_func,
                inputs=[text],
                outputs=[textboxes[key] for key in field_labels.keys()]
            )
            download_button.click(
                collect_patient_data,
                inputs=[textboxes[key] for key in field_labels.keys()],
                outputs=None
            )

# Запуск програми / Launch the app
demo.launch()
