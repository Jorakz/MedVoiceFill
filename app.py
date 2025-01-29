import gradio as gr
import app_function as func
import document_import as doci
import uvicorn

# Dictionary for field labels (remains the same as in original code)
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
    "dispensary_group_disease":"Захворювання взяття на диспансерний облік",
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

# Initialize patient_data_docx with empty strings first
patient_data = {key: '' for key in field_labels.keys()}

def collect_patient_data(*values):
    current_data = {}

    doci.docx_info_add(patient_data)
    for key, value in zip(field_labels.keys(), values):
        current_data[key] = value
    return func.download_func(current_data)

# Function to update data in dictionary
def update_patient_data(key, value):
    patient_data[key] = value
    return value


# Function to display patient data
def display_patient_data():
    output = "\n".join([f"{field_labels[key]}: {value}" for key, value in patient_data.items() if value])
    print(output)
    print(patient_data)
    print(text)
    # Return a list of values for all textboxes
    return [patient_data.get(key, '') for key in field_labels.keys()] + ["Немає даних" if not output else output]


with gr.Blocks(css=".large-textbox { font-size: 20px; }") as demo:
    gr.Markdown("# Автоматизація медичних даних")

    with gr.Row():
        with gr.Column():

            audio_input = gr.Audio(type="filepath", label="Записуйте свій голос")
            audio_processing_button = gr.Button("Обробка аудіо")
            text = gr.TextArea(label="Текст", lines=8, interactive=True)

            text_processing_button = gr.Button("Аналіз тексту")

            with gr.Row():
                download_button = gr.Button("Завантажити дані")
                clear_button = gr.Button("Очистити дані")

        with gr.Column():
            textboxes = {}  # Dictionary to store Gradio textbox components
            with gr.Row():
                with gr.Column():
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

            # Connect widgets to functions
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
            # Update download button to collect and pass current textbox values
            download_button.click(
                collect_patient_data,
                inputs=[textboxes[key] for key in field_labels.keys()],
                outputs=None
            )

# Launch the app
demo.launch()